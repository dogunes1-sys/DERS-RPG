import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="Ders RPG", layout="wide")
st.title("🎮 Ders RPG Kontrol Paneli")

try:
    if "gcp_service_account" not in st.secrets:
        st.error("Lütfen Streamlit Cloud panelinden Secrets ayarını yapın!")
    else:
        # Secrets'ı al
        creds_info = dict(st.secrets["gcp_service_account"])
        
        # --- KRİTİK DÜZELTME SATIRI ---
        # Bu satır, anahtardaki format bozukluklarını otomatik onarır.
        if "private_key" in creds_info:
            creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
        
        # Google bağlantısı
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Tabloyu aç (ID'nin doğruluğundan eminiz)
        sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
        df = pd.DataFrame(sh.get_worksheet(0).get_all_records())
        
        if not df.empty:
            st.success("✅ Bağlantı kuruldu! Veriler hazır.")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Tabloya ulaşıldı ama içinde veri bulunamadı.")

except Exception as e:
    # Hatayı daha detaylı yakalayalım
    st.error(f"❌ Hata Detayı: {e}")
    if "private_key" in str(e):
        st.info("Anahtar formatında hala bir sorun var gibi görünüyor. Lütfen Secrets kutusunu kontrol edin.")
