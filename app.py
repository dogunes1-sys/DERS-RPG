import streamlit as st
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ders RPG v4.0", page_icon="🎮", layout="centered")

# --- VERİ SAKLAMA (SESSION STATE) ---
if 'xp' not in st.session_state:
    st.session_state.xp = 0
    st.session_state.level = 1
    st.session_state.streak = 0
    st.session_state.skills = []
    st.session_state.last_loot_xp = 0

# --- FONKSİYONLAR ---
def add_xp(amount, task_name):
    # Analiz Uzmanı Yeteneği
    if "Analiz Uzmanı" in st.session_state.skills and "Denemesi" in task_name:
        amount += 50
    
    # Şans Faktörü (Kritik: 1.5x)
    roll = random.random()
    crit_chance = 0.20 if "Şanslı Zar" in st.session_state.skills else 0.10
    
    final_amount = amount
    if roll < crit_chance:
        final_amount = int(amount * 1.5)
        st.balloons()
        st.success(f"⚡ KRİTİK VURUŞ! {task_name} -> +{final_amount} XP")
    elif roll < crit_chance + 0.05:
        final_amount = amount // 2
        st.error(f"🌑 PUSU! {task_name} -> +{final_amount} XP")
    else:
        st.info(f"✨ {task_name} -> +{final_amount} XP")

    if st.session_state.streak >= 3:
        final_amount *= 2
        st.warning("🔥 COMBO BONUSU (2x)!")

    st.session_state.xp += final_amount
    st.session_state.level = (st.session_state.xp // 500) + 1

# --- ARAYÜZ ---
st.title("🎮 Ders RPG v4.0")
st.markdown("---")

col1, col2, col3 = st.columns(3)
col1.metric("⭐ Seviye", st.session_state.level)
col2.metric("📈 Toplam XP", st.session_state.xp)
col3.metric("🔥 Seri (Gün)", st.session_state.streak)

st.write(f"Level {st.session_state.level + 1} için İlerleme")
st.progress((st.session_state.xp % 500) / 500)

st.subheader("⚔️ Görevler")
tab1, tab2 = st.tabs(["Günlük", "Denemeler"])
with tab1:
    c1, c2 = st.columns(2)
    if c1.button("🎥 Mini Grind (Video) -> 15 XP", use_container_width=True): add_xp(15, "Soru Videosu")
    if c1.button("🛡️ Standart (30 dk) -> 75 XP", use_container_width=True): add_xp(75, "30dk Çalışma")
    if c2.button("⚔️ BOSS FIGHT (60 dk) -> 160 XP", use_container_width=True): add_xp(160, "Boss Fight")
    if c2.button("🏆 EPIC QUEST (Konu Bitir) -> 400 XP", use_container_width=True): add_xp(400, "Konu Bitirme")
with tab2:
    if st.button("📑 TYT DENEMESİ -> 200 XP", use_container_width=True): add_xp(200, "TYT Denemesi")
    if st.button("📑 AYT DENEMESİ -> 200 XP", use_container_width=True): add_xp(200, "AYT Denemesi")

st.subheader("✨ Yetenek Ağacı (750 XP)")
sc1, sc2 = st.columns(2)
if sc1.button("🎲 Şanslı Zar (%20 Kritik)", use_container_width=True):
    if st.session_state.xp >= 750:
        st.session_state.xp -= 750
        st.session_state.skills.append("Şanslı Zar")
        st.rerun()
if sc2.button("🧠 Analiz Uzmanı (Deneme +50 XP)", use_container_width=True):
    if st.session_state.xp >= 750:
        st.session_state.xp -= 750
        st.session_state.skills.append("Analiz Uzmanı")
        st.rerun()

st.markdown("---")
if st.button("🔥 GÜNÜ BAŞARIYLA TAMAMLA", use_container_width=True):
    st.session_state.streak += 1
    st.balloons()
