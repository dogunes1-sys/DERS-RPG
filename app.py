import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Sayfa Ayarı
st.set_page_config(page_title="Ders RPG", page_icon="🎮")

st.title("🎮 Ders RPG Kontrol Paneli")

# Bağlantıyı kur (Ayarları Secrets'tan çeker)
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Veriyi oku
    url = "https://docs.google.com/spreadsheets/d/1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8/edit?usp=sharing"
    data = conn.read(spreadsheet=url)
    
    if not data.empty:
        st.subheader("📊 Öğrenci Listesi")
        st.dataframe(data, use_container_width=True)
    else:
        st.warning("Tablo boş görünüyor.")
except Exception as e:
    st.error(f"Bağlantı hatası: {e}")
