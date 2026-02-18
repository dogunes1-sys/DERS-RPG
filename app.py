import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. ANAHTARI PARÇALARA BÖLDÜK (KARAKTER HATASI İMKANSIZ)
key_lines = [
    "-----BEGIN PRIVATE KEY-----",
    "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDrIBYK91FfqUJi",
    "+DcGVNO8X7o0mlVMhgtcGzo4IfwEgd+VWH8e2XXCJY5b873hU1lDmUT6Trts0qRf",
    "0EhKt28J7oCVvMJo4Ub4dfzMJG5VyhkTSL4agQ7aO9jglQSgqFuefNlv2upqmztK",
    "jbsk2ZWDn9yPxImjraZxh4ObhLVTu3LixikfYrKF5QtjNBHIkUSWBxvrHeysKEM9",
    "o3EDyPx43LIBUg8dbUT9CrLQNING6WJ9UHMXLEtaobv23uqW9fqI3+Y7tUMl4Cur",
    "VymM+9jWasCkoQHillD5M/1Hm1l+5lWgy49Tx4tPHKAxXrWQOs0BLePjhODAzJcp",
    "PWBApBPjAgMBAAECggEAas6MBNY9AkoGjKO5hyhAeLk5gky7Q8Q+Y8xAgaA6daez",
    "c4mcUVyySAu8Y9vQnQs6KOF2eogKTtBO9/FK7ZnvGGFdyudQnsj67sHWILvJ3TGt",
    "e1uXc729i/gUuEwpKnvgBporQcr9ooi6gc7pPL+UUhLr4+kBJzeqPLc02xAJOKu2",
    "emk74yYPdo3nAVJ/Rkg1NknWNbA6HojXdKwU/4/Qqb0SCnYvWVQBatwEW1JP11nT",
    "o48LQIfpWFXD8PAMEba8qhSGjXZN7QA7huChluXFlH9E+ybdEwuqINszsSBtQrn0",
    "qjCyFj+Uu4lVJE30oceCGDEbLgUFtoNxGC4wRdSYqQKBgQD7KrJGTxqZNZ4bR7Ux",
    "/A+3lOUTTAhJwxOxo6LmPUIGRdVKDNLpws7gTVM0tkcwhRRi/iLthWO3pfhZq6Vk",
    "HBkhrGS2n0vEYXx9E5zUu1Wulj5wx7Qw+TAwtqkglldj4jlv9qgOYc8qFUBlP5Ts",
    "CN3ah1EWPtU4fjz2UwNGAxcS6QKBgQDvpl2wjGjFL/v5gACGzMXVBr9sXvc7RqXN",
    "ufpEf3ufMWkIo0wtIKG/yESPKc7jvKL/oY0cdSAjd8mdiSSLHNQmcJPtxZ7LIQSI",
    "VHkJ3DXB8OqUm/tIOak5MnsRw2vmJBENTiadO4NCjmbkzlMbaFPhZ7H1lLCoNUYq",
    "QzbK0IT46wKBgQDmMRtylM0r3ZgqKG5IgVtmRXAtX2G5OLCz/eUuXrZESXxRga9L",
    "zt8Lc9LuXKCiN1WX5JLeXYImrlYO2OGb/qSJ2BX1yckHEtGlUHRMA+VjPQ+9DUp4",
    "F+myu7YFx8QQJyW9F7Kue7YCO7fpE3zJVtb9kUcfvDZusEPu/eXiJLLhAQKBgGur",
    "/qok26nEvlxCA3qNJFFq37SMEl5ihnohFe2SrXM/2uYToFUiNSoai5sa+KZfiYh7",
    "CBCCGzd0SXRrOqz5/eNrbztEL+0p34R1F5CzjL+fQ3YTgtnXdk2JfbvkZmUXTUYC",
    "F91K8NWFb3tbrAFDZXR/h3hEHv7kOKsiWcrT1vqTAoGAcRkF1vkGWzfyVOLz7lQ8",
    "mwlzq7SLwcHj/BMGeUBVmjtrI1NTu8tCdNwVCTIsufa3hHIBWPx+s7F+nMUwIsMBq",
    "AyTxOqXtrbbiBTFurVHcYJVdl7jQ8cmZomB0eq/hR1LdjQpMT+bosH41jyq3uU1h",
    "dBcFW0v/euIGpBbG+nTKgfs=",
    "-----END PRIVATE KEY-----"
]

# Anahtarı Python birleştirsin (\n hataları biter)
PRIVATE_KEY = "\n".join(key_lines)

SERVICE_ACCOUNT_INFO = {
    "type": "service_account",
    "project_id": "dersrpg",
    "private_key_id": "d4e4b87ab157fd2dd9a8f2aea0ea1bed5cefbe41",
    "private_key": PRIVATE_KEY,
    "client_email": "ders-rpg-bot@dersrpg.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.googleapis.com/token",
}

# 2. Uygulama Mantığı
st.set_page_config(page_title="Ders RPG", layout="wide")
st.title("🎮 Ders RPG Kontrol Paneli")

def load_data():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=scopes)
    client = gspread.authorize(creds)
    sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
    return sh.get_worksheet(0)

try:
    worksheet = load_data()
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    if not df.empty:
        st.success("✅ Bağlantı kuruldu!")
        st.dataframe(df, use_container_width=True)

        st.divider()
        st.subheader("🧙‍♂️ Kahraman Yönetimi")
        
        col1, col2 = st.columns(2)
        with col1:
            secilen = st.selectbox("Kahraman Seç:", df["ogrenci"].tolist())
        with col2:
            miktar = st.number_input("Eklenecek XP:", min_value=1, value=10)

        if st.button("✨ XP Ver"):
            row_idx = df.index[df['ogrenci'] == secilen].tolist()[0] + 2
            mevcut_xp = int(df.loc[df['ogrenci'] == secilen, 'xp'].values[0])
            worksheet.update_cell(row_idx, 2, mevcut_xp + miktar)
            st.balloons()
            st.rerun()
except Exception as e:
    st.error(f"❌ Kritik Hata: {e}")
