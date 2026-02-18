import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ders RPG v6.5", page_icon="🎮", layout="centered")

# --- GOOGLE SHEETS BAĞLANTISI ---
def get_connection():
    try:
        # JSON dosyasını manuel olarak okuyoruz
        with open("dersrpg-d4e4b87ab157.json", "r") as f:
            service_account_info = json.load(f)
        
        # Bağlantıyı bu bilgilerle kuruyoruz
        return st.connection("gsheets", type=GSheetsConnection, **service_account_info)
    except FileNotFoundError:
        st.error("Hata: 'dersrpg-d4e4b87ab157.json' dosyası GitHub'da bulunamadı!")
        return None
    except Exception as e:
        st.error(f"Bağlantı hatası: {e}")
        return None

conn = get_connection()

def load_data():
    if conn is None:
        return pd.DataFrame()
    try:
        url = "https://docs.google.com/spreadsheets/d/1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8/edit?usp=sharing"
        return conn.read(spreadsheet=url)
    except Exception as e:
        st.error(f"Veri yüklenirken hata oluştu: {e}")
        return pd.DataFrame()

# --- ANA UYGULAMA ---
st.title("🎮 Ders RPG Kontrol Paneli")

if conn:
    data = load_data()
    if not data.empty:
        st.subheader("📊 Mevcut Durum")
        st.dataframe(data, use_container_width=True)
        st.success("Bağlantı başarılı! Veriler güncel.")
    else:
        st.warning("Tablo boş veya veri çekilemedi.")
