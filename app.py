import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="Ders RPG", layout="wide")
st.title("🎮 Ders RPG Kontrol Paneli")

# Secrets kontrolü ve veri çekme
try:
    if "gcp_service_account" not in st.secrets:
        st.error("Secrets kutusunda 'gcp_service_account' başlığı bulunamadı!")
    else:
        # Secrets'ı sözlüğe çevir
        creds_info = dict(st.secrets["gcp_service_account"])
        
        # Google bağlantısı
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Tabloyu aç
        sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
        df = pd.DataFrame(sh.get_worksheet(0).get_all_records())
        
        if not df.empty:
            st.success("✅ Ejderhalar uyandı, veriler geldi!")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Bağlantı kuruldu ama tablo içi boş görünüyor.")

except Exception as e:
    st.error(f"❌ Teknik bir sorun var: {e}")
