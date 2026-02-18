import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. Bağlantı Ayarları
def get_client():
    s = st.secrets["gcp_service_account"]
    # Private key içindeki hatalı kaçış karakterlerini temizle
    private_key = s["private_key"].replace("\\n", "\n")
    
    creds_dict = {
        "type": s["type"],
        "project_id": s["project_id"],
        "private_key_id": s["private_key_id"],
        "private_key": private_key,
        "client_email": s["client_email"],
        "token_uri": s["token_uri"],
    }
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return gspread.authorize(creds)

try:
    client = get_client()
    sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
    worksheet = sh.get_worksheet(0)
    
    st.title("🎮 Ders RPG")
    
    # Verileri Çek
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        
        st.divider()
        # Basit XP Ekleme Alanı
        ogrenci = st.selectbox("Kahraman:", df["ogrenci"].tolist())
        xp_ekle = st.number_input("XP Miktarı:", min_value=1, value=10)
        
        if st.button("XP Ver!"):
            row_idx = df.index[df['ogrenci'] == ogrenci].tolist()[0] + 2
            mevcut_xp = int(df.loc[df['ogrenci'] == ogrenci, 'xp'].values[0])
            worksheet.update_cell(row_idx, 2, mevcut_xp + xp_ekle)
            st.success(f"{ogrenci} güçlendi!")
            st.rerun()
    else:
        st.warning("Tablo boş.")

except Exception as e:
    st.error(f"⚠️ Kritik Hata: {e}")
    st.info("İpucu: Eğer hala PEM hatası alıyorsan, Secrets kısmındaki private_key başında/sonunda tırnak veya boşluk kalmadığından emin ol.")
