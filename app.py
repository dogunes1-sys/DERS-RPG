import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="Ders RPG", layout="wide")
st.title("🎮 Ders RPG Kontrol Paneli")

# 1. Bağlantı Ayarları
def get_gspread_client():
    s = st.secrets["gcp_service_account"]
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
    return gspread.authorize(creds)

try:
    client = get_gspread_client()
    sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
    worksheet = sh.get_worksheet(0)
    
    # Verileri Çek
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    # Tabloyu Göster
    st.subheader("🛡️ Kahraman Durumu")
    st.dataframe(df, use_container_width=True)

    st.divider()

    # XP Yönetim Paneli
    st.subheader("🧙‍♂️ Kahraman Yönetimi")
    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            secilen_kahraman = st.selectbox("Bir Kahraman Seç:", df["ogrenci"].tolist())
        with col2:
            eklenecek_xp = st.number_input("Eklenecek XP Miktarı:", min_value=1, value=10, step=5)

        if st.button(f"✨ {secilen_kahraman} İçin XP Tanımla"):
            # Satır bul (indeks + 2 çünkü başlık var ve Google 1'den başlar)
            row_idx = df.index[df['ogrenci'] == secilen_kahraman].tolist()[0] + 2
            mevcut_xp = int(df.loc[df['ogrenci'] == secilen_kahraman, 'xp'].values[0])
            yeni_xp = mevcut_xp + eklenecek_xp
            
            # Google Sheet'i Güncelle (XP B sütununda, yani 2. sütun)
            worksheet.update_cell(row_idx, 2, yeni_xp)
            
            st.balloons()
            st.success(f"Başarılı! {secilen_kahraman} artık {yeni_xp} XP!")
            st.rerun()
    else:
        st.warning("Tabloda henüz veri bulunamadı.")

except Exception as e:
    st.error(f"Bir hata oluştu: {e}")

if st.sidebar.button("🔄 Verileri Yenile"):
    st.rerun()
