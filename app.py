import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ders RPG v6.0", page_icon="🎮", layout="centered")

# --- GOOGLE SHEETS BAĞLANTISI ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        data = conn.read(worksheet="Sheet1", ttl=0)
        if data.empty:
            return {"xp": 0, "level": 1, "streak": 0, "skills": "", "last_loot": 0}
        return data.iloc[0].to_dict()
    except:
        return {"xp": 0, "level": 1, "streak": 0, "skills": "", "last_loot": 0}

def save_data(xp, level, streak, skills, last_loot):
    df = pd.DataFrame([{
        "xp": xp, 
        "level": level, 
        "streak": streak, 
        "skills": ",".join(skills),
        "last_loot": last_loot
    }])
    conn.update(worksheet="Sheet1", data=df)

# Verileri Başlat
user_data = load_data()
if 'xp' not in st.session_state:
    st.session_state.xp = int(user_data.get('xp', 0))
    st.session_state.level = int(user_data.get('level', 1))
    st.session_state.streak = int(user_data.get('streak', 0))
    st.session_state.last_loot = int(user_data.get('last_loot', 0))
    s_val = user_data.get('skills', "")
    st.session_state.skills = s_val.split(",") if (isinstance(s_val, str) and s_val) else []

# --- ÖDÜLLER VE FONKSİYONLAR ---
LOOT_BOX = [
    "🎁 15 Dakika YouTube/Twitch Molası!",
    "🎁 1 Maç Hızlı Oyun (Valorant/LoL/CS)!",
    "🎁 En Sevdiğin İçecek/Atıştırmalık!",
    "🔥 EPİK: 45 Dakika Kesintisiz Oyun Süresi!",
    "💎 EFSANEVİ: İstediğin Bir Bölüm Dizi İzle!"
]

def add_xp(amount, task_name):
    if "Analiz Uzmanı" in st.session_state.skills and ("Deneme" in task_name or "Analiz" in task_name):
        amount += 50
    
    crit_chance = 0.20 if "Şanslı Zar" in st.session_state.skills else 0.10
    final_amount = amount
    
    if random.random() < crit_chance:
        final_amount = int(amount * 1.5)
        st.balloons()
        st.success(f"⚡ KRİTİK! {task_name} -> +{final_amount} XP")
    else:
        st.info(f"✨ {task_name} -> +{final_amount} XP")

    if st.session_state.streak >= 3:
        final_amount *= 2
        st.warning("🔥 COMBO AKTİF (2x)!")

    st.session_state.xp += final_amount
    st.session_state.level = (st.session_state.xp // 500) + 1
    save_data(st.session_state.xp, st.session_state.level, st.session_state.streak, st.session_state.skills, st.session_state.last_loot)

# --- ARAYÜZ ---
st.title("🎮 Ders RPG: Bulut Sistemi")
st.markdown(f"**Durum:** Bulut Senkronizasyonu Aktif ✅")

c1, c2, c3 = st.columns(3)
c1.metric("⭐ Seviye", st.session_state.level)
c2.metric("📈 XP", st.session_state.xp)
c3.metric("🔥 Seri", st.session_state.streak)

st.progress((st.session_state.xp % 500) / 500)

# GACHA SİSTEMİ
loot_hakki = (st.session_state.xp // 200) - (st.session_state.last_loot // 200)
if loot_hakki > 0:
    st.warning(f"🎰 {int(loot_hakki)} ADET GANİMET SANDIĞI HAZIR!")
    if st.button("🎁 SANDIĞI AÇ!", use_container_width=True):
        award = random.choice(LOOT_BOX)
        st.session_state.last_loot += 200
        save_data(st.session_state.xp, st.session_state.level, st.session_state.streak, st.session_state.skills, st.session_state.last_loot)
        st.success(f"TEBRİKLER: {award}")
        st.snow()

# GÖREVLER
tab1, tab2, tab3 = st.tabs(["Günlük Çalışma", "Deneme & Branş", "Analiz"])
with tab1:
    col_a, col_b = st.columns(2)
    if col_a.button("🎥 Mini Grind (Video) -> 15 XP", use_container_width=True): add_xp(15, "Video")
    if col_a.button("🛡️ Standart (30 dk) -> 75 XP", use_container_width=True): add_xp(75, "30dk")
    if col_b.button("⚔️ BOSS FIGHT (60 dk) -> 160 XP", use_container_width=True): add_xp(160, "Boss")
    if col_b.button("🏆 EPIC QUEST (Konu Bitir) -> 400 XP", use_container_width=True): add_xp(400, "Konu")

with tab2:
    if st.button("📑 TYT/AYT Genel Deneme -> 250 XP", use_container_width=True): add_xp(250, "Genel Deneme")
    if st.button("🧪 Branş Denemesi -> 120 XP", use_container_width=True): add_xp(120, "Branş Denemesi")

with tab3:
    if st.button("🔍 Deneme Analizi -> 100 XP", use_container_width=True): add_xp(100, "Analiz")
    if st.button("🧹 Soru Temizliği (10 Soru) -> 40 XP", use_container_width=True): add_xp(40, "Soru")

# SKILL TREE
st.subheader("✨ Yetenek Ağacı")
s1, s2 = st.columns(2)
if "Şanslı Zar" in st.session_state.skills: s1.success("✅ Şanslı Zar")
elif s1.button("🎲 Şanslı Zar (750 XP)", use_container_width=True):
    if st.session_state.xp >= 750:
        st.session_state.xp -= 750; st.session_state.skills.append("Şanslı Zar")
        save_data(st.session_state.xp, st.session_state.level, st.session_state.streak, st.session_state.skills, st.session_state.last_loot); st.rerun()

if "Analiz Uzmanı" in st.session_state.skills: s2.success("✅ Analiz Uzmanı")
elif s2.button("🧠 Analiz Uzmanı (750 XP)", use_container_width=True):
    if st.session_state.xp >= 750:
        st.session_state.xp -= 750; st.session_state.skills.append("Analiz Uzmanı")
        save_data(st.session_state.xp, st.session_state.level, st.session_state.streak, st.session_state.skills, st.session_state.last_loot); st.rerun()

if st.button("🔥 GÜNÜ KAPAT", use_container_width=True):
    st.session_state.streak += 1
    save_data(st.session_state.xp, st.session_state.level, st.session_state.streak, st.session_state.skills, st.session_state.last_loot)
    st.balloons()
