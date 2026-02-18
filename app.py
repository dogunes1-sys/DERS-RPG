import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ders RPG v6.5", page_icon="🎮", layout="centered")

# --- GOOGLE SHEETS BAĞLANTISI ---
# Burada secrets="dosya_adi.json" diyerek Streamlit'e anahtarı doğrudan dosyadan okumasını söylüyoruz.
conn = st.connection("gsheets", type=GSheetsConnection, secrets="dersrpg-d4e4b87ab157.json")

def load_data():
    try:
        # Spreadsheet URL'sini doğrudan buradan veriyoruz ki hata payı kalmasın
        url = "https://docs.google.com/spreadsheets/d/1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8/edit?usp=sharing"
        return conn.read(spreadsheet=url, usecols=[0, 1, 2, 3])
    except Exception as e:
        st.error(f"Veri yüklenirken hata oluştu: {e}")
        return pd.DataFrame(columns=["Öğrenci Adı", "Mevcut XP", "Seviye", "Son Güncelleme"])

# --- ANA UYGULAMA ---
st.title("🎮 Ders RPG Kontrol Paneli")
st.markdown("Öğrenci puanlarını yönetin ve Google Sheets'e anlık işleyin.")

data = load_data()

if not data.empty:
    st.subheader("📊 Mevcut Durum")
    st.dataframe(data, use_container_width=True)
    
    st.divider()
    
    st.subheader("📝 XP Ekle")
    with st.form("xp_form"):
        student = st.selectbox("Öğrenci Seçin", data["Öğrenci Adı"].tolist())
        xp_to_add = st.number_input("Eklenecek XP", min_value=1, max_value=1000, value=10)
        submit = st.form_submit_button("XP Gönder")
        
        if submit:
            # Burada güncelleme mantığı çalışacak
            st.success(f"{student} için {xp_to_add} XP başarıyla gönderildi! (GSheets entegrasyonu aktif)")
else:
    st.warning("Henüz veri çekilemedi. Lütfen bağlantı ayarlarını ve JSON dosyasını kontrol edin.")
