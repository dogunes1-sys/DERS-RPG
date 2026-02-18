import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="Ders RPG", layout="wide")

# Secrets'tan bilgileri al
try:
    creds_dict = dict(st.secrets["gcp_service_account"])
    # Bağlantıyı kur
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    
    # Tabloyu oku
    sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
    df = pd.DataFrame(sh.get_worksheet(0).get_all_records())
    
    st.title("🎮 Ders RPG Kontrol Paneli")
    st.success("✅ Bağlantı başarılı!")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.title("🎮 Ders RPG Kontrol Paneli")
    st.error(f"❌ Bağlantı hatası: {e}")
    st.info("İpucu: Secrets kutusundaki formatı kontrol edin.")
