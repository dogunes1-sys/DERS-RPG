import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Ders RPG v6.5", page_icon="🎮")

st.title("🎮 Ders RPG Kontrol Paneli")

# Bağlantıyı oluştur (Ayarları otomatik olarak Secrets'tan çeker)
conn = st.connection("gsheets", type=GSheetsConnection)

# Google Sheets URL'si
url = "https://docs.google.com/spreadsheets/d/1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8/edit?usp=sharing"

try:
    # Veriyi oku
    df = conn.read(spreadsheet=url)
    
    if not df.empty:
        st.subheader("📊 Öğrenci Durum Listesi")
        st.dataframe(df, use_container_width=True)
        st.success("Veriler başarıyla güncellendi.")
    else:
        st.warning("Veri çekildi ancak tablo boş görünüyor.")
        
except Exception as e:
    st.error("❌ Bağlantı Kurulamadı!")
    st.info("Lütfen Secrets alanındaki private_key formatının doğru olduğunu kontrol edin.")
    # Hatayı teknik olarak görmek istersen burayı açabilirsin:
    # st.write(e)
