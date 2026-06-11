# app.py
import streamlit as st
import random
from datetime import datetime
from FSM import BeautyFSM
from engine import NLPEngine

# ==========================================
# 1. KONFIGURASI HALAMAN & CSS PREMIUM ERP
# ==========================================
st.set_page_config(page_title="Aura Clinic ERP", page_icon="💎", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #FAFAFA; }
    
    .main-header {
        background: linear-gradient(135deg, #D81B60 0%, #FF8A80 100%);
        padding: 25px; border-radius: 15px; color: white; margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(216, 27, 96, 0.15);
    }
    
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: white; padding: 10px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.02); }
    .stTabs [data-baseweb="tab"] { border-radius: 8px !important; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #FFF0F5 !important; color: #D81B60 !important; font-weight: 700 !important; }

    .katalog-card {
        background: white; padding: 25px; border-radius: 20px; border: 1px solid #FCE4EC; text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease; height: 100%;
    }
    .katalog-card:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(216, 27, 96, 0.08); }
    .stChatMessage { background-color: white; border-radius: 18px; border: 1px solid #F5F5F5; padding: 15px; }
    .badge-confirmed { background-color: #E8F5E9; color: #2E7D32; padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INISIALISASI DATABASE & STATE (SAFE MODE)
# ==========================================
if 'bot' not in st.session_state or st.sidebar.button("🔄 Reset Memori & Database"):
    st.session_state.bot = BeautyFSM()
    st.session_state.nlp_master = NLPEngine()
    st.session_state.chat_history = [{"role": "assistant", "content": st.session_state.bot.get_response()}]
    st.session_state.database_pasien = [
        {
            "code": "AURA-8821", 
            "name": "Clarissa Utama", 
            "treatment": {"name": "Laser Hollywood Glow", "price": 600000}, 
            "schedule": "Besok, 10:00 WIB", 
            "doctor": "Dr. Sarah Sp.DV", 
            "skin_type": "Oily", 
            "status": "Confirmed",
            "date_created": datetime.now().strftime("%Y-%m-%d")
        }
    ]
    st.sidebar.success("Memori dibersihkan!")

# ==========================================
# 3. SIDEBAR BRANDING
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #D81B60;'>💎 AURA CLINIC</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Enterprise Medical System</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("👨‍💻 **Sistem Terintegrasi**\n\nMenghubungkan NLP Chatbot dengan Data Panel Resepsionis.")
    st.success("🤖 **Engine Status:**\n\n🟢 FSM & RegEx Online")
    st.markdown("---")
    st.caption("Final Project Smt 6 © 2024")

# ==========================================
# 4. KONTEN UTAMA
# ==========================================
st.markdown("""
<div class="main-header">
    <h1 style="color: white; margin: 0;">Sistem Manajemen Klinik Terpadu</h1>
    <p style="margin: 0; font-size: 16px; opacity: 0.9;">Solusi Digital Reservasi Pasien berbasis Kecerdasan Buatan (Automata)</p>
</div>
""", unsafe_allow_html=True)

tab_bot, tab_katalog, tab_form, tab_admin = st.tabs([
    "🤖 Smart AI Chatbot", 
    "🛍️ Layanan Medis", 
    "📋 Registrasi Manual", 
    "📊 ERP Administrator"
])

# ------------------------------------------
# TAB 1: CHATBOT AI (PROTEKSI TOTAL)
# ------------------------------------------
with tab_bot:
    c_chat, c_info = st.columns([7, 3])
    
    with c_chat:
        st.markdown("### 💬 Konsultasi Dokter Digital")
        chat_container = st.container(height=400)
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
        
        if user_query := st.chat_input("Ketik keluhan kulit Anda di sini..."):
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            
            try:
                booking_sukses = st.session_state.bot.step(user_query)
                
                if booking_sukses and isinstance(booking_sukses, dict):
                    if "treatment" in booking_sukses and isinstance(booking_sukses["treatment"], str):
                        t_nama = booking_sukses["treatment"]
                        booking_sukses["treatment"] = {"name": t_nama, "price": 350000}
                    
                    if "code" not in booking_sukses: booking_sukses["code"] = f"AURA-{random.randint(1000, 9999)}"
                    if "status" not in booking_sukses: booking_sukses["status"] = "Confirmed"
                    if "doctor" not in booking_sukses: booking_sukses["doctor"] = "Dr. Sarah Sp.DV"
                    if "date_created" not in booking_sukses: booking_sukses["date_created"] = datetime.now().strftime("%Y-%m-%d")
                    
                    st.session_state.database_pasien.append(booking_sukses)
            except Exception as e:
                pass
                
            st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.bot.get_response()})
            st.rerun()

    with c_info:
        st.markdown("### 🔬 Diagnostic Tools")
        uploaded_file = st.file_uploader("Upload Foto Wajah", type=['jpg', 'png', 'jpeg'])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Menganalisis tekstur...", use_column_width=True)
            st.success("Foto berhasil diunggah!")
        st.markdown("---")
        st.markdown("### ⚙️ Sistem Log FSM")
        try:
            st.info(f"📍 **State Aktif:** `{st.session_state.bot.state.name}`")
        except:
            st.info(f"📍 **State Aktif:** `RUNNING`")

# ------------------------------------------
# TAB 2: KATALOG Layanan
# ------------------------------------------
with tab_katalog:
    st.markdown("### 🌟 Katalog Perawatan Premium")
    menu = st.session_state.nlp_master.treatment_data
    col1, col2 = st.columns(2)
    for i, (key, data) in enumerate(menu.items()):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            st.markdown(f"""
            <div class="katalog-card">
                <h1 style='font-size: 50px; margin:0;'>{data['emoji']}</h1>
                <h3 style='color: #D81B60; margin-top: 10px;'>{data['name']}</h3>
                <p style='color: gray; font-size: 14px;'>{data['desc']}</p>
                <hr style='border: 0.5px solid #FCE4EC;'>
                <p>⏱ <b>Durasi:</b> {data['duration']} <br> 💰 <b>Harga:</b> <span style='color: #D81B60; font-weight: 800; font-size: 18px;'>Rp {data['price']:,}</span></p>
            </div>
            <br>
            """, unsafe_allow_html=True)

# ------------------------------------------
# TAB 3: FORM MANUAL
# ------------------------------------------
with tab_form:
    st.markdown("### 📝 Pendaftaran Pasien Offline")
    with st.form("manual_booking_form", clear_on_submit=True):
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            f_name = st.text_input("👤 Nama Lengkap Pasien")
            f_doctor = st.selectbox("👨‍⚕️ Dokter Penanggung Jawab", ["Dr. Sarah Sp.DV", "Dr. Kevin Sp.DV", "Rina (Aesthetician)"])
            f_date = st.date_input("📅 Tanggal Kedatangan")
        with f_col2:
            list_treatment_names = [t["name"] for t in st.session_state.nlp_master.treatment_data.values()]
            f_treatment_name = st.selectbox("💉 Pilih Tindakan", list_treatment_names)
            f_skin_type = st.selectbox("🧬 Klasifikasi Kulit", ["Normal", "Dry", "Oily", "Sensitive", "Combination"])
            f_time = st.time_input("⏰ Jam Tindakan")
            
        st.markdown("---")
        submit_btn = st.form_submit_button("💾 Simpan & Terbitkan E-Ticket", use_container_width=True)
        if submit_btn:
            if f_name.strip() == "":
                st.error("Nama pasien wajib diisi!")
            else:
                selected_t_obj = next(t for t in st.session_state.nlp_master.treatment_data.values() if t["name"] == f_treatment_name)
                new_booking = {
                    "code": f"AURA-{random.randint(1000, 9999)}", "name": f_name,
                    "treatment": selected_t_obj, "schedule": f"{f_date.strftime('%d %B %Y')} ({f_time.strftime('%H:%M')})",
                    "doctor": f_doctor, "skin_type": f_skin_type, "status": "Confirmed",
                    "date_created": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.database_pasien.append(new_booking)
                st.success(f"Pasien {f_name} berhasil didaftarkan!")

# ------------------------------------------
# TAB 4: ADMIN DASHBOARD (PENGAMAN BERLAPIS ANTI-KEYERROR)
# ------------------------------------------
with tab_admin:
    st.markdown("### 📈 Executive Analytics Dashboard")
    
    total_pasien = 0
    total_omset = 0
    valid_pasien_list = []
    
    # Membaca data menggunakan .get() aman agar tidak memicu KeyError apa pun bentuk datanya
    if 'database_pasien' in st.session_state:
        for p in st.session_state.database_pasien:
            if isinstance(p, dict):
                total_pasien += 1
                valid_pasien_list.append(p)
                t_data = p.get("treatment", {})
                if isinstance(t_data, dict):
                    total_omset += t_data.get("price", 0)
                elif isinstance(t_data, (int, float)):
                    total_omset += t_data
                
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("👥 Total Pasien", f"{total_pasien} Orang")
    m2.metric("💰 Estimasi Omset", f"Rp {total_omset:,.0f}")
    m3.metric("📈 Growth Ratio", "+12.5%")
    m4.metric("⭐ Kepuasan", "4.9/5")
    
    st.markdown("---")
    st.markdown("#### 🗂️ Antrean Master Data Pasien")
    
    for pasien in valid_pasien_list:
        p_name = pasien.get("name", "Pasien Anonim")
        p_code = pasien.get("code", "AURA-XXXX")
        p_status = pasien.get("status", "Confirmed")
        p_doctor = pasien.get("doctor", "Belum Ditentukan")
        p_sched = pasien.get("schedule", "Hari Ini")
        p_date = pasien.get("date_created", datetime.now().strftime("%Y-%m-%d")) # <- AMAN DARI KEYERROR
        
        t_data = pasien.get("treatment", {})
        t_name = t_data.get("name", "Perawatan Kulit") if isinstance(t_data, dict) else "Perawatan"
        t_price = t_data.get("price", 0) if isinstance(t_data, dict) else 0
        
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 15px; border-left: 6px solid #D81B60; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h4 style="margin: 0; color: #333;">{p_name} <span style="font-size: 14px; font-weight: normal; color: gray;">({p_code})</span></h4>
                <span class="badge-confirmed">{str(p_status).upper()}</span>
            </div>
            <div style="display: flex; gap: 30px; font-size: 14px; color: #555;">
                <div><b>Tindakan:</b> {t_name}</div>
                <div><b>Jadwal:</b> {p_sched}</div>
                <div><b>Dokter:</b> {p_doctor}</div>
                <div><b>Tanggal Input:</b> {p_date}</div>
                <div style="color: #D81B60; font-weight: bold;">Rp {t_price:,}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)