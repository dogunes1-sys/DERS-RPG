import streamlit as st
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ders RPG v4.0", page_icon="🎮", layout="centered")

# --- KALICI OLMAYAN HAFIZA (Sayfa Yenilenince Sıfırlanır) ---
# Gerçek kayıt için bir sonraki adımda Google Sheets bağlayacağız.
if 'xp' not in st.session_state:
    st.session_state.xp = 0
    st.session_state.level = 1
    st.session_state.streak = 0
    st.session_state.skills = []

# --- XP EKLEME FONKSİYONU ---
def add_xp(amount, task_name):
    # Analiz Uzmanı Yeteneği
    if "Analiz Uzmanı" in st.session_state.skills and "Denemesi" in task_name:
        amount += 50
    
    # Şans Faktörü (Kritik: 1.5x, Pusu: 0.5x)
    roll = random.random()
    crit_chance = 0.20 if "Şanslı Zar" in st.session_state.skills else 0.10
    
    final_amount = amount
    if roll < crit_chance:
        final_amount = int(amount * 1.5)
        st.balloons()
        st.success(f"⚡ KRİTİK VURUŞ! {task_name} -> +{final_amount} XP")
    elif roll < crit_chance + 0.05:
        final_amount = amount // 2
        st.error(f"🌑 PUSUYA DÜŞTÜN! {task_name} -> +{final_amount} XP")
    else:
        st.info(f"✨ {task_name} Tamamlandı! +{final_amount} XP")

    # Seri (Combo) Bonusu (3 gün ve üzeri için 2x)
    if st.session_state.streak >= 3:
        final_amount *= 2
        st.warning("🔥 COMBO BONUSU (2x XP Aktif)!")

    st.session_state.xp += final_amount
    st.session_state.level = (st.session_state.xp // 500) + 1

# --- ARAYÜZ TASARIMI ---
st.title("🎮 Ders RPG: Dopamin Engine")
st.markdown("---")

# Oyuncu Durumu
col1, col2, col3 = st.columns(3)
col1.metric("⭐ Seviye", st.session_state.level)
col2.metric("📈 Toplam XP", st.session_state.xp)
col3.metric("🔥 Seri (Gün)", st.session_state.streak)

# Level İlerleme Barı
current_level_xp = st.session_state.xp % 500
progress = current_level_xp / 500
st.write(f"Level {st.session_state.level + 1} için İlerleme (%{int(progress*100)})")
st.progress(progress)

# GÖREVLER
st.subheader("⚔️ Görev Listesi")
tab1, tab2 = st.tabs(["Günlük Görevler", "Haftalık Denemeler"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎥 Mini Grind (Video) -> 15 XP", use_container_width=True): add_xp(15, "Soru Videosu")
        if st.button("🛡️ Standart Görev (30 dk) -> 75 XP", use_container_width=True): add_xp(75, "30dk Çalışma")
    with c2:
        if st.button("⚔️ BOSS FIGHT (60 dk) -> 160 XP", use_container_width=True): add_xp(160, "Boss Fight")
        if st.button("🏆 EPIC QUEST (Konu Bitir) -> 400 XP", use_container_width=True): add_xp(400, "Konu Bitirme")

with tab2:
    if st.button("📑 TYT DENEMESİ -> 200 XP", use_container_width=True): add_xp(200, "TYT Denemesi")
    if st.button("📑 AYT DENEMESİ -> 200 XP", use_container_width=True): add_xp(200, "AYT Denemesi")

# SKILL TREE
st.subheader("✨ Yetenek Ağacı (Bedel: 750 XP)")
sc1, sc2 = st.columns(2)

# Şanslı Zar
if "Şanslı Zar" in st.session_state.skills:
    sc1.success("✅ Şanslı Zar Aktif")
else:
    if sc1.button("🎲 Şanslı Zar (%20 Kritik Vuruş)", use_container_width=True):
        if st.session_state.xp >= 750:
            st.session_state.xp -= 750
            st.session_state.skills.append("Şanslı Zar")
            st.rerun()
        else: st.error("XP Yetersiz!")

# Analiz Uzmanı
if "Analiz Uzmanı" in st.session_state.skills:
    sc2.success("✅ Analiz Uzmanı Aktif")
else:
    if sc2.button("🧠 Analiz Uzmanı (Deneme +50 XP)", use_container_width=True):
        if st.session_state.xp >= 750:
            st.session_state.xp -= 750
            st.session_state.skills.append("Analiz Uzmanı")
            st.rerun()
        else: st.error("XP Yetersiz!")

# GÜNÜ KAPAT
st.markdown("---")
if st.button("🔥 BUGÜNÜ TAMAMLA (Seri Artır)", use_container_width=True):
    st.session_state.streak += 1
    st.balloons()
    st.toast("Seri güncellendi!")
