import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import re

st.set_page_config(page_title="Ders RPG", layout="wide")
st.title("🎮 Ders RPG Kontrol Paneli")

def sanitize_private_key(key_contents):
    """Anahtar içindeki tüm format bozukluklarını (boşluk, alt çizgi, \n) temizler."""
    if not key_contents:
        return ""
    
    # 1. Adım: Başlık ve sonu ayır, ortadaki base64 kısmını al
    # Tüm \n, \\n ve boşlukları temizle
    clean_content = key_contents.replace("-----BEGIN PRIVATE KEY-----", "")
    clean_content = clean_content.replace("-----END PRIVATE KEY-----", "")
    clean_content = clean_content.replace("\\n", "").replace("\n", "").replace(" ", "").strip()
    
    # 2. Adım: Google'ın beklediği 64 karakterlik satırlara böl
    lines = [clean_content[i:i+64] for i in range(0, len(clean_content), 64)]
    
    # 3. Adım: Başlık ve sonu tertemiz şekilde yeniden inşa et
    formatted_key = "-----BEGIN PRIVATE KEY-----\n" + "\n".join(lines) + "\n-----END PRIVATE KEY-----\n"
    return formatted_key

try:
    if "gcp_service_account" not in st.secrets:
        st.error("Secrets kutusu boş!")
    else:
        # Secrets'tan bilgileri al
        creds_info = dict(st.secrets["gcp_service_account"])
        
        # ANAHTARI AMELİYAT ET
        raw_key = creds_info.get("private_key", "")
        creds_info["private_key"] = sanitize_private_key(raw_key)
        
        # Google bağlantısı
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Tabloyu aç
        sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
        df = pd.DataFrame(sh.get_worksheet(0).get_all_records())
        
        st.success("✅ BAĞLANTI BAŞARILI! Veriler aşağıda:")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"❌ Hala bir sorun var: {e}")
    st.info("İpucu: Eğer hala PEM hatası veriyorsa, Secrets kutusunda 'private_key' değerinin tırnak içinde olduğundan emin olun.")
