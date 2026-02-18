import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ders RPG v6.5", page_icon="🎮", layout="centered")

# --- GOOGLE SHEETS BAĞLANTISI ---
# JSON dosyasını GitHub'a yüklediğinde bu satır çalışacak
conn = st.connection("gsheets", type=GSheetsConnection, secrets="dersrpg-d4e4b87ab157.json")

def load_data():
    try:
        url = "https://docs.google.com/spreadsheets/d/1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8/edit?usp=sharing"
        # Senin tablonun sütun isimlerine göre okuyoruz
        return conn.read(spreadsheet=url)
    except Exception as e:
        st.error(f"Veri yüklenirken hata oluştu: {e}")
        return pd.DataFrame()

# --- ANA UYGULAMA ---
st.title("🎮 Ders RPG Kontrol Paneli")

data = load_data()

if not data.empty:
    st.subheader("📊 Mevcut Durum")
    st.dataframe(data, use_container_width=True)
    
    st.divider()
    
    st.subheader("📝 İşlem Yap")
    # Sheets'teki ilk sütuna göre (xp sütunu gibi) işlem yapalım
    st.info("Veriler başarıyla çekildi. Artık butonlarla XP ekleme mantığını kurabiliriz.")
else:
    st.warning("Veri çekilemedi. Lütfen JSON dosyasını GitHub'a yüklediğinizden emin olun.")
