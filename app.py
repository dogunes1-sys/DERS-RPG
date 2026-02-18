import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="Ders RPG", layout="wide", page_icon="🎮")
st.title("🎮 Ders RPG Kontrol Paneli")

# Bağlantı Fonksiyonu
def get_worksheet():
    try:
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
        sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
        return sh.get_worksheet(0)
    except Exception as e:
        st.error(f"Bağlantı hatası: {e}")
        return None

worksheet = get_worksheet()

if worksheet:
    # Verileri çek ve DataFrame yap
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    if df.empty:
        st.warning("Tablo bağlı ama içinde veri bulunamadı. Lütfen Google Sheet'e bir satır veri ekleyin.")
    else:
        st.success("✅ Ejderhalar evcilleştirildi! Veriler yayında.")
        st.dataframe(df, use_container_width=True)

        st.divider()
        st.subheader("🧙‍♂️ Kahraman Yönetimi")

        # XP Verme Arayüzü
        col1, col2 = st.columns(2)
        
        with col1:
            secilen_ogrenci = st.selectbox("Bir Kahraman Seç:", df["ogrenci"].tolist())
        
        with col2:
            eklenecek_xp = st.number_input("Eklenecek XP:", min_value=1, value=10, step=5)

        if st.button(f"✨ {secilen_ogrenci}'e {eklenecek_xp} XP Tanımla"):
            try:
                # İsmin kaçıncı satırda olduğunu bul (Başlık dahil olduğu için +2)
                row_idx = df.index[df['ogrenci'] == secilen_ogrenci].tolist()[0] + 2
                
                # Mevcut XP'yi al ve yenisini ekle
                current_xp = int(df.loc[df['ogrenci'] == secilen_ogrenci, 'xp'].values[0])
                new_xp = current_xp + eklenecek_xp
                
                # Google Sheet'te XP sütunu 2. sütun (B sütunu)
                worksheet.update_cell(row_idx, 2, new_xp)
                
                st.balloons()
                st.toast(f"{secilen_ogrenci} artık daha güçlü! Yeni XP: {new_xp}")
                st.rerun() # Sayfayı yenileyerek güncel tabloyu çek
            except Exception as e:
                st.error(f"XP eklenirken hata oluştu: {e}")

if st.sidebar.button("🔄 Verileri Zorla Yenile"):
    st.rerun()
