# FSM.py
from engine import NLPEngine

class State:
    def __init__(self, name):
        self.name = name

class BeautyFSM:
    def __init__(self):
        self.STATE_IDLE = State("IDLE")
        self.STATE_REKOMENDASI = State("REKOMENDASI")
        self.STATE_BOOKING = State("BOOKING")
        
        self.state = self.STATE_IDLE
        self.nlp = NLPEngine()
        self.current_treatment = None
        self.current_concern = "Belum Diidentifikasi"
        self.detected_skin_type = "Normal (Normal Skin)"
        self.response = "Halo! Saya BeautyBot, digital consultant Anda 🤖✨ Ada keluhan kulit yang ingin dikonsultasikan? Atau ketik 'booking' untuk langsung memesan treatment."
        
        # =========================================================
        # PENGATUR JADWAL & MULTI-DOKTER OTOMATIS
        # =========================================================
        self.current_hour = 10  # Jam mulai klinik (10:00)
        self.current_minute = 0 # Menit mulai klinik (10:00)
        
        # Daftar Dokter Spesialis Klinik Anda
        self.daftar_dokter = ["Dr. Sarah Sp.DV", "Dr. Angelica Sp.DV", "Dr. Rian Sp.DV"]
        self.dokter_index = 0   # Pointer untuk menandai giliran dokter

    def get_response(self):
        return self.response

    def step(self, user_input):
        text = user_input.strip().lower()
        
        if text in ["reset", "menu", "halo", "hi", "restart"]:
            self.state = self.STATE_IDLE
            self.current_treatment = None
            self.current_concern = "Belum Diidentifikasi"
            self.detected_skin_type = "Normal (Normal Skin)"
            self.response = "Sistem direset! Silakan ceritakan keluhan kulit Anda kembali atau ketik 'booking'."
            return None

        # ---------------------------------------------------------
        # 1. STATE: IDLE
        # ---------------------------------------------------------
        if self.state == self.STATE_IDLE:
            if text == "booking":
                self.state = self.STATE_BOOKING
                self.response = "Pilihan yang tepat! Untuk melakukan reservasi klinik, silakan ketik nama lengkap Anda (Contoh: 'nana ika'):"
                return None
                
            kategori = self.nlp.ekstrak_keluhan(text)
            self.detected_skin_type = self.nlp.deteksi_tipe_kulit(text)
            
            if kategori and kategori in self.nlp.treatment_data:
                self.current_treatment = self.nlp.treatment_data[kategori]
                self.current_concern = kategori.replace("_", " ").title()
                
                self.state = self.STATE_REKOMENDASI
                self.response = f"""🩺 **Hasil Analisis Keluhan Medis:**
                
* ⚠️ **Keluhan Utama:** Kulit mengalami masalah **{self.current_concern}**
* 🧬 **Prediksi Tipe Kulit:** {self.detected_skin_type}

---

💡 **Solusi Tindakan Klinik Yang Direkomendasikan:**
* 💉 **Treatment:** *{self.current_treatment['name']}* {self.current_treatment['emoji']}
* 📋 **Cara Kerja:** {self.current_treatment['desc']}
* 💰 **Biaya:** Rp {self.current_treatment['price']:,}
* ⏱️ **Durasi:** {self.current_treatment['duration']}

Apakah Anda ingin mengambil tindakan ini? Ketik **'booking'** untuk mengamankan antrean jadwal dokter!"""
                return None
            else:
                self.response = "Maaf, BeautyBot belum mendeteksi kata kunci keluhan tersebut. Coba ceritakan masalah wajah Anda secara spesifik."
                return None

        # ---------------------------------------------------------
        # 2. STATE: REKOMENDASI
        # ---------------------------------------------------------
        elif self.state == self.STATE_REKOMENDASI:
            if "book" in text or text in ["ya", "mau", "ok", "oke", "tertarik"]:
                self.state = self.STATE_BOOKING
                self.response = "Pilihan yang tepat! Untuk melakukan reservasi klinik, silakan ketik nama lengkap Anda (Contoh: 'nana ika'):"
                return None
            else:
                self.state = self.STATE_IDLE
                self.response = "Konsultasi dialihkan. Silakan ceritakan keluhan kulit Anda yang lain atau ketik 'booking'."
                return None

        # ---------------------------------------------------------
        # 3. STATE: BOOKING (Sistem Pembagian Beban Dokter & Waktu)
        # ---------------------------------------------------------
        elif self.state == self.STATE_BOOKING:
            nama_pasien = user_input.strip()
            
            if nama_pasien.lower() == "booking" or nama_pasien == "":
                self.response = "Mohon masukkan nama lengkap Anda untuk dicetak pada kartu pasien klinik:"
                return None

            if not self.current_treatment:
                self.current_treatment = self.nlp.treatment_data["jerawat"]
                self.current_concern = "Jerawat"
                
            # --- 1. LOGIKA PILIH DOKTER BERGILIRAN (ROUND ROBIN) ---
            dokter_terpilih = self.daftar_dokter[self.dokter_index]
            
            # Geser indeks dokter untuk pasien berikutnya
            self.dokter_index += 1
            if self.dokter_index >= len(self.daftar_dokter):
                self.dokter_index = 0 # Balik lagi ke dokter pertama jika sudah penuh
                
            # --- 2. LOGIKA MAJUKAN SLOT JADWAL ANTRIAN ---
            jam_mulai = f"{self.current_hour:02d}:{self.current_minute:02d}"
            
            self.current_minute += 30
            if self.current_minute >= 60:
                self.current_hour += 1
                self.current_minute = 0
                
            jam_selesai = f"{self.current_hour:02d}:{self.current_minute:02d}"
            jadwal_final = f"Besok, Jam {jam_mulai} - {jam_selesai} WIB"
            # --------------------------------------------------------
            
            # Paket Data Rekam Medis Akhir untuk ERP Admin Dashboard
            data_final = {
                "name": nama_pasien,
                "treatment": self.current_treatment,
                "schedule": jadwal_final,
                "doctor": dokter_terpilih, # <--- SEKARANG DOKTERNYA BERGANTI OTOMATIS!
                "skin_type": f"{self.detected_skin_type} (Keluhan: {self.current_concern})",
                "status": "Confirmed"
            }
            
            self.response = f"""🎉 **RESERVASI KLINIK BERHASIL!** 🎉
            
Data rekam medis atas nama **{nama_pasien}** telah dikirim ke Panel Resepsionis. 
* 🩺 **Keluhan Ditangani:** {self.current_concern}
* 👩‍⚕️ **Dokter Penanggung Jawab:** {dokter_terpilih}
* ⏱️ **Slot Waktu Anda:** {jadwal_final}

Silakan menuju tab **'ERP Administrator'** untuk melihat e-ticket antrean Anda. Sampai jumpa di Aura Clinic! ✨"""
            
            self.state = self.STATE_IDLE
            return data_final

        return None