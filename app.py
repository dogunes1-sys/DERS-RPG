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
        # Google Sheet ID
        sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
        return sh.get_worksheet(0)
    except Exception as e:
        st.error(f"Bağlantı hatası: {e}")
        return None

worksheet = get_worksheet()

if worksheet:
    # Verileri ham liste olarak çek (Daha güvenlidir)
    all_values = worksheet.get_all_values()
    
    if len(all_values) > 1:
        # İlk satırı başlık, kalanları veri yap
        headers = [str(h).strip() for h in all_values[0]]
        rows = all_values[1:]
        df = pd.DataFrame(rows, columns=headers)
        
        st.success("✅ Bağlantı aktif! Kahramanlar hazır.")
        st.dataframe(df, use_container_width=True)

        st.divider()
        st.subheader("🧙‍♂️ Kahraman Yönetimi")

        # XP Verme İşlemi
        col1, col2 = st.columns(2)
        
        # Sütun isimlerini kontrol ederek (ogrenci ve xp) işlem yap
        if "ogrenci" in df.columns and "xp" in df.columns:
            with col1:
                secilen = st.selectbox("Bir Kahraman Seç:", df["ogrenci"].tolist())
            with col2:
                miktar = st.number_input("Eklenecek XP:", min_value=1, value=10)

            if st.button(f"✨ {secilen}'e XP Gönder"):
                try:
                    # Satır numarasını bul (indis 0 + başlık satırı + 1 = row_idx)
                    row_idx = df.index[df['ogrenci'] == secilen].tolist()[0] + 2
                    
                    # Mevcut XP'yi sayıya çevir
                    current_xp = int(df.loc[df['ogrenci'] == secilen, 'xp'].values[0])
                    new_xp = current_xp + miktar
                    
                    # XP sütunu B sütunu (2. sütun)
                    worksheet.update_cell(row_idx, 2, str(new_xp))
                    
                    st.balloons()
                    st.success(f"{secilen} artık {new_xp} XP!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Güncelleme yapılamadı: {e}")
        else:
            st.error("Hata: Google Sheet'te 'ogrenci' veya 'xp' başlığı bulunamadı!")
    else:
        st.warning("Bağlantı başarılı ama tabloda başlık dışında veri yok.")

if st.sidebar.button("🔄 Verileri Yenile"):
    st.rerun()
