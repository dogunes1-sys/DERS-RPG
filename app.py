import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="Ders RPG", layout="wide")
st.title("🎮 Ders RPG Kontrol Paneli")

# Bağlantı Fonksiyonu
def load_data():
    try:
        # Secrets'tan verileri çek
        s = st.secrets["gcp_service_account"]
        creds_dict = {
            "type": s["type"],
            "project_id": s["project_id"],
            "private_key_id": s["private_key_id"],
            "private_key": s["private_key"].replace("\\n", "\n"),
            "client_email": s["client_email"],
            "token_uri": s["token_uri"],
        }
        
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Tablo ID
        sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
        worksheet = sh.get_worksheet(0)
        return pd.DataFrame(worksheet.get_all_records()), None
    except Exception as e:
        return None, str(e)

# Veriyi yükle
df, error = load_data()

if error:
    st.error(f"❌ Bağlantı Hatası: {error}")
    st.info("Lütfen Secrets ayarlarını kaydedip Reboot yapın.")
else:
    st.success("✅ Başarıyla bağlandı!")
    st.dataframe(df, use_container_width=True)

if st.sidebar.button("Yenile"):
    st.rerun()
