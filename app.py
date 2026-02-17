import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ders RPG v5.1", page_icon="🎰", layout="centered")

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

# Verileri yükle
user_data = load_data()

# Session State
if 'xp' not in st.session_state:
    st.session_state.xp = int(user_data['xp'])
    st.session_state.level = int(user_data['level'])
    st.session_state.streak = int(user_data['streak'])
    st.session_state.last_loot = int(user_data['last_loot'])
    st.session_state.skills = user_data['skills'].split(",") if user_data['skills'] else []

# --- GACHA ÖDÜLLERİ ---
LOOT_BOX = [
    "🎁 15 Dakika YouTube/Twitch Molası!",
    "🎁 1 Maç Hızlı Oyun (Valorant/LoL/CS)!",
    "🎁 En Sevdiğin İçecek/Kahve Ismarlama!",
    "🎁 10 Dakika Sosyal Medya Turu!",
    "🔥 EPİK: 45 Dakika Kesintisiz Oyun Süresi!",
    "💎 EFSANEVİ: İstediğin Bir Bölüm Dizi İzle!"
]

# --- FONKSİYONLAR ---
def add_xp(amount, task_name):
    if "Analiz Uzmanı" in st.session_state.skills and ("Deneme" in task_name or "Analiz" in task_name):
        amount += 50
    
    crit = 0.20 if "Şanslı Zar" in st.session_state.skills else 0.10
    final_amount = amount
    if random.random() < crit:
        final_amount = int(amount * 1.5)
        st.balloons()
    
    if st.session_state.streak >= 3:
        final_amount *= 2

    st.session_state.xp += final_amount
    st.session_state.level = (st.session_state.xp // 500) + 1
    save_data(st.session_state.xp, st.session_state.level, st.session_state.streak, st.session_state.skills, st.session_state.last_loot)

# --- ARAYÜZ ---
st.title("🎮 Ders RPG: Gacha Update")

# Durum Kartları
c1, c2, c3 = st.columns(3)
c1.metric("⭐ Seviye", st.session_state.level)
c2.metric("📈 XP", st.session_state.xp)
c3.metric("🔥 Seri", st.session_state.streak)

# --- GACHA SİSTEMİ ---
st.markdown("---")
# Her 200 XP'de bir loot hakkı
loot_hakki = (st.session_state.xp // 200) - (st.session_state.last_loot // 200)

if loot_hakki > 0:
    st.warning(f"🎰 {int(loot_hakki)} ADET GANİMET SANDIĞI HAZIR!")
    if st.button("🎁 SANDIĞI AÇ!", use_container_width=True):
        award = random.choice(LOOT_BOX)
        st.session_state.last_loot += 200
        save_data(st.session_state.xp, st.session_state.level, st.session_state.streak, st.session_state.skills, st.session_state.last_loot)
        st.success(f"TEBRİKLER! ÇIKAN ÖDÜL: \n### {award}")
        st.snow()
else:
    st.info(f"📦 Sonraki Ganimet Sandığı: **{int(st.session_state.last_loot + 200)} XP**")

st.markdown("---")

# Görev Sekmeleri (Aynı şekilde devam)
tab1, tab2, tab3 = st.tabs(["Günlük", "Deneme & Branş", "Analiz"])
with tab1:
    col_a, col_b = st.columns(2)
    if col_a.button("🎥 Mini Grind -> 15 XP", use_container_width=True): add_xp(15, "Video")
    if col_a.button("🛡️ Standart -> 75 XP", use_container_width=True): add_xp(75, "30dk")
    if col_b.button("⚔️ BOSS FIGHT -> 160 XP", use_container_width=True): add_xp(160, "Boss")
    if col_b.button("🏆 EPIC QUEST -> 400 XP", use_container_width=True): add_xp(400, "Konu")

with tab2:
    if st.button("📑 Genel Deneme -> 250 XP", use_container_width=True): add_xp(250, "Genel Deneme")
    if st.button("🧪 Branş Denemesi -> 120 XP", use_container_width=True): add_xp(120, "Branş Denemesi")

with tab3:
    if st.button("🔍 Deneme Analizi -> 100 XP", use_container_width=True): add_xp(100, "Analiz")
    if st.button("🧹 Soru Temizliği -> 40 XP", use_container_width=True): add_xp(40, "Soru")

# Skill Tree
st.subheader("✨ Yetenek Ağacı")
s1, s2 = st.columns(2)
if s1.button("🎲 Şanslı Zar (750 XP)", use_container_width=True):
    if st.session_state.xp >= 750 and "Şanslı Zar" not in st.session_state.skills:
        st.session_state.xp -= 750; st.session_state.skills.append("Şanslı Zar")
        save_data(st.session_state.xp, st.session_state.level, st.session_state.streak, st.session_state.skills, st.session_state.last_loot)
        st.rerun()

if s2.button("🧠 Analiz Uzmanı (750 XP)", use_container_width=True):
    if st.session_state.xp >= 750 and "Analiz Uzmanı" not in st.session_state.skills:
        st.session_state.xp -= 750; st.session_state.skills.append("Analiz Uzmanı")
        save_data(st.session_state.xp, st.session_state.level, st.session_state.streak, st.session_state.skills, st.session_state.last_loot)
        st.rerun()

if st.button("🔥 GÜNÜ KAPAT", use_container_width=True):
    st.session_state.streak += 1
    save_data(st.session_state.xp, st.session_state.level, st.session_state.streak, st.session_state.skills, st.session_state.last_loot)
    st.balloons()
