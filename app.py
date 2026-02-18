import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="Ders RPG", layout="wide")
st.title("🎮 Ders RPG Kontrol Paneli")

# --- VERİ ÇEKME FONKSİYONU ---
@st.cache_data(ttl=60)
def get_data():
    try:
        # Bilgileri Secrets'tan çekiyoruz
        creds_dict = st.secrets["gcp_service_account"]
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Tablo ID
        sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
        df = pd.DataFrame(sh.get_worksheet(0).get_all_records())
        return df, None
    except Exception as e:
        return None, str(e)

# --- ANA EKRAN ---
df, error = get_data()

if error:
    st.error(f"⚠️ Bağlantı Başarısız: {error}")
    st.info("Secrets ayarlarını kontrol edin.")
elif df is not None:
    st.success("✨ Veriler başarıyla getirildi!")
    st.dataframe(df, use_container_width=True)

if st.sidebar.button("Verileri Zorla Yenile"):
    st.cache_data.clear()
    st.rerun()
