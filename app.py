import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="Ders RPG", layout="wide")
st.title("🎮 Ders RPG Kontrol Paneli")

# --- KİMLİK BİLGİLERİ ---
# Anahtarın içine manuel \n ekleyerek formatı koruyoruz
raw_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDrIBYK91FfqUJi\n+DcGVNO8X7o0mlVMhgtcGzo4IfwEgd+VWH8e2XXCJY5b873hU1lDmUT6Trts0qRf\n0EhKt28J7oCVvMJo4Ub4dfzMJG5VyhkTSL4agQ7aO9jglQSgqFuefNlv2upqmztK\njbsk2ZWDn9yPxImjraZxh4ObhLVTu3LixikfYrKF5QtjNBHIkUSWBxvrHeysKEM9\no3EDyPx43LIBUg8dbUT9CrLQNING6WJ9UHMXLEtaobv23uqW9fqI3+Y7tUMl4Cur\nVymM+9jWasCkoQHillD5M/1Hm1l+5lWgy49Tx4tPHKAxXrWQOs0BLePjhODAzJcp\nPWBApBPjAgMBAAECggEAas6MBNY9AkoGjKO5hyhAeLk5gky7Q8Q+Y8xAgaA6daez\nc4mcUVyySAu8Y9vQnQs6KOF2eogKTtBO9/FK7ZnvGGFdyudQnsj67sHWILvJ3TGt\ne1uXc729i/gUuEwpKnvgBporQcr9ooi6gc7pPL+UUhLr4+kBJzeqPLc02xAJOKu2\nemk74yYPdo3nAVJ/Rkg1NknWNbA6HojXdKwU/4/Qqb0SCnYvWVQBatwEW1JP11nT\no48LQIfpWFXD8PAMEba8qhSGjXZN7QA7huChluXFlH9E+ybdEwuqINszsSBtQrn0\nqjCyFj+Uu4lVJE30oceCGDEbLgUFtoNxGC4wRdSYqQKBgQD7KrJGTxqZNZ4bR7Ux\n/A+3lOUTTAhJwxOxo6LmPUIGRdVKDNLpws7gTVM0tkcwhRRi/iLthWO3pfhZq6Vk\nHBkhrGS2n0vEYXx9E5zUu1Wulj5wx7Qw+TAwtqkglldj4jlv9qgOYc8qFUBlP5Ts\nCN3ah1EWPtU4fjz2UwNGAxcS6QKBgQDvpl2wjGjFL/v5gACGzMXVBr9sXvc7RqXN\nufpEf3ufMWkIo0wtIKG/yESPKc7jvKL/oY0cdSAjd8mdiSSLHNQmcJPtxZ7LIQSI\nVHkJ3DXB8OqUm/tIOak5MnsRw2vmJBENTiadO4NCjmbkzlMbaFPhZ7H1lLCoNUYq\nQzbK0IT46wKBgQDmMRtylM0r3ZgqKG5IgVtmRXAtX2G5OLCz/eUuXrZESXxRga9L\nzt8Lc9LuXKCiN1WX5JLeXYImrlYO2OGb/qSJ2BX1yckHEtGlUHRMA+VjPQ+9DUp4\nF+myu7YFx8QQJyW9F7Kue7YCO7fpE3zJVtb9kUcfvDZusEPu/eXiJLLhAQKBgGur\n/qok26nEvlxCA3qNJFFq37SMEl5ihnohFe2SrXM/2uYToFUiNSoai5sa+KZfiYh7\nCBCCGzd0SXRrOqz5/eNrbztEL+0p34R1F5CzjL+fQ3YTgtnXdk2JfbvkZmUXTUYC\nF91K8NWFb3tbrAFDZXR/h3hEHv7kOKsiWcrT1vqTAoGAcRkF1vkGWzfyVOLz7lQ8\nwlzq7SLwcHj/BMGeUBVmjtrI1NTu8tCdNwVCTIsufa3hHIBWPx+s7F+nMUwIsMBq\nAyTxOqXtrbbiBTFurVHcYJVdl7jQ8cmZomB0eq/hR1LdjQpMT+bosH41jyq3uU1h\ndBcFW0v/euIGpBbG+nTKgfs=\n-----END PRIVATE KEY-----"

service_account_info = {
    "type": "service_account",
    "project_id": "dersrpg",
    "private_key": raw_key,
    "client_email": "ders-rpg-bot@dersrpg.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.googleapis.com/token",
}

# --- VERİ ÇEKME ---
def load_data():
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Senin Spreadsheet ID'n
        sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
        worksheet = sh.get_worksheet(0)
        return pd.DataFrame(worksheet.get_all_records())
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        return pd.DataFrame()

# --- ARAYÜZ ---
df = load_data()

if not df.empty:
    st.success("✅ Veriler Google Sheets'ten çekildi!")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Tablo şu an boş veya bağlantı kuruluyor...")
