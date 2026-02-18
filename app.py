import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Sayfa Ayarı
st.set_page_config(page_title="Ders RPG", layout="wide")

def get_client():
    # Secrets'tan veriyi çek
    s = st.secrets["gcp_service_account"]
    
    # Private key'deki çift ters eğik çizgileri temizle ve gerçek satır sonu yap
    raw_key = s["private_key"]
    clean_key = raw_key.replace("\\n", "\n")
    
    creds_dict = {
        "type": s["type"],
        "project_id": s["project_id"],
        "private_key_id": s["private_key_id"],
        "private_key": clean_key,
        "client_email": s["client_email"],
        "token_uri": s["token_uri"],
    }
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return gspread.authorize(creds)

try:
    client = get_client()
    # Senin Sheet ID'n
    sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
    worksheet = sh.get_worksheet(0)
    
    st.title("🎮 Ders RPG Paneli")
    
    # Verileri oku
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    
    if not df.empty:
        st.success("Bağlantı başarılı!")
        st.dataframe(df, use_container_width=True)
        
        st.divider()
        st.subheader("🧙‍♂️ XP İşlemleri")
        
        col1, col2 = st.columns(2)
        with col1:
            secilen = st.selectbox("Öğrenci Seç:", df["ogrenci"].tolist())
        with col2:
            miktar = st.number_input("Eklenecek XP:", min_value=1, value=10)
            
        if st.button("XP Gönder"):
            # Google Sheet'te satır bul (indeks + 2)
            row_idx = df.index[df['ogrenci'] == secilen].tolist()[0] + 2
            mevcut_xp = int(df.loc[df['ogrenci'] == secilen, 'xp'].values[0])
            worksheet.update_cell(row_idx, 2, mevcut_xp + miktar)
            st.balloons()
            st.success(f"{secilen} için XP güncellendi!")
            st.rerun()
    else:
        st.warning("Tablo boş görünüyor.")

except Exception as e:
    st.error(f"Hata detayı: {e}")
