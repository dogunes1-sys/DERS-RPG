import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import re

st.set_page_config(page_title="Ders RPG", layout="wide")
st.title("🎮 Ders RPG Kontrol Paneli")

def clean_key(key):
    # Anahtar içindeki hatalı kaçış karakterlerini ve gizli boşlukları temizler
    if not key: return ""
    key = key.replace("\\n", "\n")
    # Eğer anahtar tek satır geldiyse, her 64 karakterde bir satır başı ekleyerek onarır
    if "-----BEGIN PRIVATE KEY-----" in key and "\n" not in key[28:-26]:
        header = "-----BEGIN PRIVATE KEY-----\n"
        footer = "\n-----END PRIVATE KEY-----"
        content = key.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "").replace(" ", "").replace("\n", "")
        content = "\n".join(re.findall('.{1,64}', content))
        key = header + content + footer
    return key

try:
    if "gcp_service_account" not in st.secrets:
        st.error("Secrets bulunamadı!")
    else:
        creds_info = dict(st.secrets["gcp_service_account"])
        # Anahtarı temizleme fonksiyonundan geçiriyoruz
        creds_info["private_key"] = clean_key(creds_info.get("private_key", ""))
        
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
        client = gspread.authorize(creds)
        
        sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
        df = pd.DataFrame(sh.get_worksheet(0).get_all_records())
        
        if not df.empty:
            st.success("✨ Bağlantı kuruldu! Öğrenci verileri yüklendi.")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("⚠️ Tabloya bağlanıldı ama içerik boş. Lütfen 2. satıra bir veri ekleyin!")

except Exception as e:
    st.error(f"❌ Bağlantı Hatası: {e}")
