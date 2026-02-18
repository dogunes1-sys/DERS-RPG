import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🎮 Ders RPG Kontrol Paneli")

# Bağlantı
conn = st.connection("gsheets", type=GSheetsConnection)

# URL (Senin tablon)
url = "https://docs.google.com/spreadsheets/d/1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8/edit?usp=sharing"

# Veriyi oku ve göster
try:
    data = conn.read(spreadsheet=url)
    st.dataframe(data)
except Exception as e:
    st.error(f"Hata: {e}")
