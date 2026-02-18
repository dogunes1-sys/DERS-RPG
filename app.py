import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Ders RPG", layout="centered")
st.title("🎮 Ders RPG Kontrol Paneli")

# --- KİMLİK BİLGİLERİ (DOĞRUDAN KODUN İÇİNDE) ---
# Secrets panelindeki hataları baypas etmek için bilgileri buraya güvenli sözlük olarak alıyoruz.
creds = {
    "type": "service_account",
    "project_id": "dersrpg",
    "private_key_id": "d4e4b87ab157fd2dd9a8f2aea0ea1bed5cefbe41",
    "private_key": "-----BEGIN PRIVATE KEY-----\n"
                   "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDrIBYK91FfqUJi\n"
                   "+DcGVNO8X7o0mlVMhgtcGzo4IfwEgd+VWH8e2XXCJY5b873hU1lDmUT6Trts0qRf\n"
                   "0EhKt28J7oCVvMJo4Ub4dfzMJG5VyhkTSL4agQ7aO9jglQSgqFuefNlv2upqmztK\n"
                   "jbsk2ZWDn9yPxImjraZxh4ObhLVTu3LixikfYrKF5QtjNBHIkUSWBxvrHeysKEM9\n"
                   "o3EDyPx43LIBUg8dbUT9CrLQNING6WJ9UHMXLEtaobv23uqW9fqI3+Y7tUMl4Cur\n"
                   "VymM+9jWasCkoQHillD5M/1Hm1l+5lWgy49Tx4tPHKAxXrWQOs0BLePjhODAzJcp\n"
                   "PWBApBPjAgMBAAECggEAas6MBNY9AkoGjKO5hyhAeLk5gky7Q8Q+Y8xAgaA6daez\n"
                   "c4mcUVyySAu8Y9vQnQs6KOF2eogKTtBO9/FK7ZnvGGFdyudQnsj67sHWILvJ3TGt\n"
                   "e1uXc729i/gUuEwpKnvgBporQcr9ooi6gc7pPL+UUhLr4+kBJzeqPLc02xAJOKu2\n"
                   "emk74yYPdo3nAVJ/Rkg1NknWNbA6HojXdKwU/4/Qqb0SCnYvWVQBatwEW1JP11nT\n"
                   "o48LQIfpWFXD8PAMEba8qhSGjXZN7QA7huChluXFlH9E+ybdEwuqINszsSBtQrn0\n"
                   "qjCyFj+Uu4lVJE30oceCGDEbLgUFtoNxGC4wRdSYqQKBgQD7KrJGTxqZNZ4bR7Ux\n"
                   "/A+3lOUTTAhJwxOxo6LmPUIGRdVKDNLpws7gTVM0tkcwhRRi/iLthWO3pfhZq6Vk\n"
                   "HBKhrGS2n0vEYXx9E5zUu1Wulj5wx7Qw+TAwtqkglldj4jlv9qgOYc8qFUBlP5Ts\n"
                   "CN3ah1EWPtU4fjz2UwNGAxcS6QKBgQDvpl2wjGjFL/v5gACGzMXVBr9sXvc7RqXN\n"
                   "ufpEf3ufMWkIo0wtIKG/yESPKc7jvKL/oY0cdSAjd8mdiSSLHNQmcJPtxZ7LIQSI\n"
                   "VHkJ3DXB8OqUm/tIOak5MnsRw2vmJBENTiadO4NCjmbkzlMbaFPhZ7H1lLCoNUYq\n"
                   "QzbK0IT46wKBgQDmMRtylM0r3ZgqKG5IgVtmRXAtX2G5OLCz/eUuXrZESXxRga9L\n"
                   "zt8Lc9LuXKCiN1WX5JLeXYImrlYO2OGb/qSJ2BX1yckHEtGlUHRMA+VjPQ+9DUp4\n"
                   "F+myu7YFx8QQJyW9F7Kue7YCO7fpE3zJVtb9kUcfvDZusEPu/eXiJLLhAQKBgGur\n"
                   "/qok26nEvlxCA3qNJFFq37SMEl5ihnohFe2SrXM/2uYToFUiNSoai5sa+KZfiYh7\n"
                   "CBCCGzd0SXRrOqz5/eNrbztEL+0p34R1F5CzjL+fQ3YTgtnXdk2JfbvkZmUXTUYC\n"
                   "F91K8NWFb3tbrAFDZXR/h3hEHv7kOKsiWcrT1vqTAoGAcRkF1vkGWzfyVOLz7lQ8\n"
                   "wlzq7SLwcHj/BMGeUBVmjtrI1NTu8tCdNwVCTIsufa3hHIBWPx+s7F+nMUwIsMBq\n"
                   "AyTxOqXtrbbiBTFurVHcYJVdl7jQ8cmZomB0eq/hR1LdjQpMT+bosH41jyq3uU1h\n"
                   "dBcFW0v/euIGpBbG+nTKgfs=\n"
                   "-----END PRIVATE KEY-----",
    "client_email": "ders-rpg-bot@dersrpg.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.googleapis.com/token",
}

# --- BAĞLANTI ---
try:
    # Secrets kullanmadan doğrudan creds sözlüğünü gönderiyoruz
    conn = st.connection("gsheets", type=GSheetsConnection, **creds)
    
    url = "https://docs.google.com/spreadsheets/d/1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8/edit?usp=sharing"
    df = conn.read(spreadsheet=url)

    if not df.empty:
        st.subheader("📊 Öğrenci Listesi")
        st.dataframe(df, use_container_width=True)
        st.balloons() # Başarıyla yüklenirse küçük bir kutlama
    else:
        st.warning("Veri çekildi ama tablo boş.")

except Exception as e:
    st.error("Bağlantı sırasında bir hata oluştu.")
    st.code(e) # Hatayı açıkça görelim
