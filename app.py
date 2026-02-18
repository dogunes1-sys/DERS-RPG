import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="Ders RPG", layout="wide")

def get_worksheet():
    # Secrets'tan bilgileri çek
    s = st.secrets["gcp_service_account"]
    
    # Credentials sözlüğünü oluştur
    creds_dict = {
        "type": s["type"],
        "project_id": s["project_id"],
        "private_key_id": s["private_key_id"],
        "private_key": s["private_key"],
        "client_email": s["client_email"],
        "token_uri": s["token_uri"],
    }
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    
    # Tabloyu aç
    sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
    return sh.get_worksheet(0)

st.title("🎮 Ders RPG Paneli")

try:
    worksheet = get_worksheet()
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    if not df.empty:
        st.success("✅ Bağlantı kuruldu!")
        st.dataframe(df, use_container_width=True)

        st.divider()
        st.subheader("🧙‍♂️ XP Yönetimi")
        
        col1, col2 = st.columns(2)
        with col1:
            secilen = st.selectbox("Bir Kahraman Seç:", df["ogrenci"].tolist())
        with col2:
            miktar = st.number_input("Eklenecek XP:", min_value=1, value=10)

        if st.button("✨ XP Tanımla"):
            row_idx = df.index[df['ogrenci'] == secilen].tolist()[0] + 2
            mevcut_xp = int(df.loc[df['ogrenci'] == secilen, 'xp'].values[0])
            worksheet.update_cell(row_idx, 2, mevcut_xp + miktar)
            st.balloons()
            st.success(f"{secilen} güncellendi!")
            st.rerun()

except Exception as e:
    st.error(f"⚠️ Hata: {e}")

if st.sidebar.button("🔄 Yenile"):
    st.rerun()
