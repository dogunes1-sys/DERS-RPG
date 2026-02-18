import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. Bağlantı Ayarları (Çalışan Mevcut Yapın)
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

# 2. Tabloyu Aç
sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
worksheet = sh.get_worksheet(0)

# 3. Veriyi Çek ve Göster
st.title("🎮 Ders RPG Kontrol Paneli")
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Tabloyu göster
st.subheader("🛡️ Kahraman Durumu")
st.dataframe(df, use_container_width=True)

st.divider()

# 4. XP Yönetim Paneli
st.subheader("🧙‍♂️ Kahraman Yönetimi")
col1, col2 = st.columns(2)

with col1:
    # Google Sheet'teki 'ogrenci' sütunundan isimleri çek
    secilen_kahraman = st.selectbox("Bir Kahraman Seç:", df["ogrenci"].tolist())

with col2:
    eklenecek_xp = st.number_input("Eklenecek XP Miktarı:", min_value=1, value=10, step=5)

if st.button(f"✨ {secilen_kahraman} İçin XP Tanımla"):
    try:
        # Satır numarasını bul (indeks + başlık satırı + 1 = row_idx)
        row_idx = df.index[df['ogrenci'] == secilen_kahraman].tolist()[0] + 2
        
        # Mevcut XP'yi al ve yenisiyle topla
        mevcut_xp = int(df.loc[df['ogrenci'] == secilen_kahraman, 'xp'].values[0])
        yeni_xp = mevcut_xp + eklenecek_xp
        
        # Google Sheet'te XP sütununu (B sütunu yani 2. sütun) güncelle
        worksheet.update_cell(row_idx, 2, yeni_xp)
        
        st.balloons() # Kutlama efekti!
        st.success(f"Başarılı! {secilen_kahraman} artık {yeni_xp} XP gücünde.")
        st.rerun() # Sayfayı yenile ki tablo güncellensin
    except Exception as e:
        st.error(f"Hata oluştu: {e}")

if st.sidebar.button("🔄 Verileri Yenile"):
    st.rerun()
