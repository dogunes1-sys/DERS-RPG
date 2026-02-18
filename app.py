import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="Ders RPG", layout="wide")
st.title("🎮 Ders RPG Kontrol Paneli")

# Bağlantı Fonksiyonu
def get_data():
    try:
        creds_info = dict(st.secrets["gcp_service_account"])
        # Anahtardaki \n karakterlerini düzelt
        creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
        
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Senin Tablo ID'n
        sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
        worksheet = sh.get_worksheet(0)
        return worksheet, pd.DataFrame(worksheet.get_all_records())
    except Exception as e:
        return None, str(e)

worksheet, result = get_data()

if isinstance(result, str):
    st.error(f"❌ Bağlantı Hatası: {result}")
else:
    st.success("✅ Ejderhalar evcilleştirildi! Veriler yayında.")
    st.dataframe(result, use_container_width=True)

    # BASİT ETKİLEŞİM PANELİ
    st.divider()
    st.subheader("🧙‍♂️ Kahraman İşlemleri")
    
    if not result.empty:
        ogrenci_adi = st.selectbox("Bir Kahraman Seç:", result["ogrenci"].tolist())
        miktar = st.number_input("Eklenecek XP Miktarı:", min_value=1, value=10)
        
        if st.button(f"{ogrenci_adi}'e {miktar} XP Gönder!"):
            # Gerçekten tabloya yazma işlemi (Bir sonraki adımda tam aktif edeceğiz)
            st.balloons()
            st.write(f"🎉 Harika! {ogrenci_adi} için {miktar} XP yollandı. (Tabloyu manuel yenileyin)")
    else:
        st.info("Tabloya veri eklendiğinde burada işlem yapabileceksin.")

if st.sidebar.button("Verileri Yenile"):
    st.rerun()
