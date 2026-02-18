import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. Bağlantı Ayarları
s = st.secrets["gcp_service_account"]
creds_dict = {
    "type": s["type"],
    "project_id": s["project_id"],
    "private_key_id": s["private_key_id"],
    "private_key": s["private_key"].replace("\\n", "\n"),
    "client_email": s["client_email"],
    "token_uri": s["token_uri"],
}

scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(creds)

# 2. Tabloyu Aç
# Senin Sheet ID'n: 1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8
sh = client.open_by_key("1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8")
worksheet = sh.get_worksheet(0)

# 3. Ekrana Bas
st.title("Ders RPG")
data = worksheet.get_all_records()
df = pd.DataFrame(data)
st.table(df)
