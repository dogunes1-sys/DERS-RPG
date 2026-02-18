import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Sayfa konfigürasyonu
st.set_page_config(page_title="Ders RPG", layout="wide")

def connect_to_sheet():
    # Secrets'tan verileri al
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
    
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    
    # Sheet'i aç
    return client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8").get_worksheet(0)

st.title("🎮 Ders RPG Kontrol Paneli")

try:
    worksheet = connect_to_sheet()
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    if not df.empty:
        st.success("✅ Sisteme başarıyla giriş yapıldı!")
        st.dataframe(df, use_container_width=True)

        st.divider()
        st.subheader("🧙‍♂️ Kahraman Yönetimi")

        col1, col2 = st.columns(2)
        with col1:
            secilen = st.selectbox("Bir Kahraman Seç:", df["ogrenci"].tolist())
        with col2:
            miktar = st.number_input("Eklenecek XP:", min_value=1, value=10, step=5)

        if st.button(f"✨ {secilen}'e XP Tanımla"):
            # Satır indeksini bul (+2: 1 başlık satırı, 1 de Google Sheet 1'den başladığı için)
            row_idx = df.index[df['ogrenci'] == secilen].tolist()[0] + 2
            mevcut_xp = int(df.loc[df['ogrenci'] == secilen, 'xp'].values[0])
            
            # Google Sheet B sütununu (2. sütun) güncelle
            worksheet.update_cell(row_idx, 2, mevcut_xp + miktar)
            
            st.balloons()
            st.success("Güç toplandı! Tablo güncelleniyor...")
            st.rerun()
    else:
        st.warning("Veritabanında henüz kahraman yok.")

except Exception as e:
    st.error(f"Kritik Hata: {e}")

if st.sidebar.button("🔄 Verileri Tazele"):
    st.rerun()
