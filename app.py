import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="Ders RPG", layout="wide")
st.title("🎮 Ders RPG Kontrol Paneli")

# Bağlantı Fonksiyonu
def connect_to_sheet():
    try:
        # Secrets'tan verileri al
        creds_info = dict(st.secrets["gcp_service_account"])
        
        # Anahtardaki gizli karakterleri temizle
        creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
        
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Tabloyu ID ile aç
        sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
        worksheet = sh.get_worksheet(0)
        data = worksheet.get_all_records()
        return pd.DataFrame(data), None
    except Exception as e:
        return None, str(e)

# Ana Ekran
df, error = connect_to_sheet()

if error:
    st.error(f"❌ Hata: {error}")
else:
    if df.empty:
        st.warning("✅ Bağlantı başarılı ama tablo şu an boş!")
        st.info("Lütfen Google Sheet'te başlıkların altına (A2, B2 gibi) veri ekleyin.")
    else:
        st.success("✨ Veriler başarıyla yüklendi!")
        st.dataframe(df, use_container_width=True)

if st.sidebar.button("Yenile"):
    st.rerun()
