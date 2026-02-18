import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🎮 Ders RPG Kontrol Paneli")

# En sade bağlantı şekli
conn = st.connection("gsheets", type=GSheetsConnection)

url = "https://docs.google.com/spreadsheets/d/1NJob3RNvMZ43_JlG1hnaZmnF_I3bUW3BtW9bsNx6kB8/edit?usp=sharing"
data = conn.read(spreadsheet=url)

st.dataframe(data)
