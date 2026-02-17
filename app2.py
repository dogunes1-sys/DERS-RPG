import streamlit as st
import random

# Verileri Streamlit Cloud'un "Secret" veya "KV" yapısında tutmak yerine 
# en basit haliyle tarayıcıda tutuyoruz. 
# KALICI OLMASI İÇİN: Streamlit Community Cloud üzerinde "Google Sheets" bağlantısı kurmalıyız.

if 'xp' not in st.session_state:
    st.session_state.xp = 0
    st.session_state.level = 1
    st.session_state.streak = 0
    st.session_state.skills = []

def add_xp(amount, task):
    # Kritik Vuruş (1.5x)
    crit = 0.20 if "Şanslı Zar" in st.session_state.skills else 0.10
    if random.random() < crit:
        amount = int(amount * 1.5)
        st.balloons()
        st.success(f"⚡ KRİTİK! {task} -> +{amount} XP")
    else:
        st.info(f"✨ {task} -> +{amount} XP")
        
    st.session_state.xp += amount
    st.session_state.level = (st.session_state.xp // 500) + 1

st.title("🎮 Ders RPG v4.0")
st.metric("Level", st.session_state.level, f"{st.session_state.xp} Toplam XP")

if st.button("🏆 Konu Bitirme (400 XP)"): add_xp(400, "Konu Bitirme")
if st.button("📑 TYT Denemesi (200 XP)"): add_xp(200, "TYT")
if st.button("📑 AYT Denemesi (200 XP)"): add_xp(200, "AYT")
if st.button("🎥 Soru Videosu (15 XP)"): add_xp(15, "Video")