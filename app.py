import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import base64
import json

st.set_page_config(page_title="Ders RPG", layout="wide")

def get_worksheet():
    # 1. Base64 formatındaki veriyi çek
    b64_data = st.secrets["gcp_service_account"]["base64_creds"]
    
    # 2. Base64'ü çöz ve JSON'a çevir (Hata payı sıfır)
    creds_json = base64.b64decode(b64_data).decode("utf-8")
    creds_dict = json.loads(creds_json)
    
    # 3. Bağlantıyı kur
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    
    sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
    return sh.get_worksheet(0)

st.title("🎮 Ders RPG Kontrol Paneli")

try:
    worksheet = get_worksheet()
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    if not df.empty:
        st.success("✅ Sisteme girildi! PEM hatası Base64 ile aşıldı.")
        st.dataframe(df, use_container_width=True)

        st.divider()
        st.subheader("🧙‍♂️ Kahraman Yönetimi")
        
        col1, col2 = st.columns(2)
        with col1:
            secilen = st.selectbox("Kahraman Seç:", df["ogrenci"].tolist())
        with col2:
            miktar = st.number_input("Eklenecek XP:", min_value=1, value=10)

        if st.button("✨ XP Gönder"):
            row_idx = df.index[df['ogrenci'] == secilen].tolist()[0] + 2
            mevcut_xp = int(df.loc[df['ogrenci'] == secilen, 'xp'].values[0])
            worksheet.update_cell(row_idx, 2, mevcut_xp + miktar)
            st.balloons()
            st.success(f"{secilen} artık daha güçlü!")
            st.rerun()
except Exception as e:
    st.error(f"⚠️ Hata: {e}")

if st.sidebar.button("🔄 Yenile"):
    st.rerun()
