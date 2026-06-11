# engine.py

class NLPEngine:
    def __init__(self):
        # Database Kamus Keluhan - Bahasa Gaul & Istilah Skincare Anak Muda
        self.keywords = {
            "jerawat": [
                "jerawat", "berjerawat", "bruntusan", "pruntusan", "pimple", "acne", "breakout", 
                "gradakan", "geradakan", "mateng", "nanah", "meradang", "jerawatan", "bisulan",
                "papul", "pustul", "maskne", "muka rusak", "tekstur"
            ],
            "kusam": [
                "kusam", "kusem", "gelap", "belang", "hitam", "butek", "burik", "dekil", 
                "tidak cerah", "ga glowing", "kurang cerah", "buluk", "muka cape", "lelah",
                "hiperpigmentasi", "dark spot", "gosong"
            ],
            "flek_hitam": [
                "flek", "flek hitam", "noda hitam", "bekas jerawat", "pie", "pih", "melasma", 
                "kerutan", "kerut", "tua", "garis halus", "kendur", "wrinkle", "bintik hitam", 
                "penuaan", "anti aging", "smile line"
            ],
            "pori_komedo": [
                "komedo", "pori", "pori-pori", "berminyak", "sebum", "lepek", "kilang minyak", 
                "kulit jeruk", "oily", "greasy", "minyakan", "blackhead", "whitehead", "pores",
                "sumbat"
            ],
            "skin_barrier": [
                "sensitif", "merah", "kemerahan", "perih", "iritasi", "gatal", "mengelupas", 
                "ngelupas", "breakout parah", "skin barrier", "rusak", "perih", "panas", 
                "dry", "kering kerontang", "ketarik"
            ]
        }
        
        # Database Layanan Medis Realistis (2 Tindakan per Kategori Keluhan)
        self.treatment_data = {
            "jerawat": {
                "name": "Acne Intensive Laser Therapy & Salicylic Peel",
                "emoji": "🛡️",
                "desc": "Kombinasi Blue Light Laser untuk mematikan bakteri penyebab jerawat dari dalam, dipadukan dengan pengolesan asam salisilat medis untuk menguras bruntusan gradakan.",
                "price": 350000,
                "duration": "60 menit"
            },
            "kusam": {
                "name": "Hollywood Glow Laser Peel & Vitamin C Meso",
                "emoji": "✨",
                "desc": "Medical laser menggunakan carbon lotion untuk mengangkat sel kulit mati yang tebal, dipadukan dengan penetrasi serum Vitamin C dosis tinggi agar wajah instan cerah bercahaya.",
                "price": 500000,
                "duration": "45 menit"
            },
            "flek_hitam": {
                "name": "Ultimate Pigmentation & Collagen RF Repair",
                "emoji": "⏳",
                "desc": "Terapi gelombang Radio Frequency (RF) untuk memudarkan melasma/flek hitam menahun, menstimulasi kolagen baru, serta mengencangkan kerutan halus di wajah.",
                "price": 650000,
                "duration": "75 menit"
            },
            "pori_komedo": {
                "name": "Pore Purifying Hydra-Vacuum & Cryo Tightening",
                "emoji": "💧",
                "desc": "Pembersihan komedo mendalam menggunakan tekanan cairan osmotik, dilanjutkan dengan cooling therapy suhu -5°C untuk membekukan kelenjar minyak dan merapatkan pori.",
                "price": 300000,
                "duration": "50000"
            },
            "skin_barrier": {
                "name": "Skin Barrier Soothing & Intense IPL Redness Therapy",
                "emoji": "🌱",
                "desc": "Penetrasi serum Ceramide murni menggunakan gelombang ultrasound untuk memperbaiki kulit mengelupas dan perih, dikombinasikan dengan spektrum cahaya IPL untuk meredakan kemerahan.",
                "price": 280000,
                "duration": "40 menit"
            }
        }

    def ekstrak_keluhan(self, text):
        """Mencocokkan input teks user dengan kamus keluhan gaul"""
        text = text.lower()
        for kategori, kata_kunci in self.keywords.items():
            for kata in kata_kunci:
                if kata in text:
                    return kategori
        return None

    def deteksi_tipe_kulit(self, text):
        """Mendeteksi tipe kulit bawaan berdasarkan kata kunci anak muda"""
        text = text.lower()
        if any(kata in text for range_kata in [self.keywords["pori_komedo"]] for kata in range_kata):
            return "Berminyak (Oily Skin)"
        elif any(kata in text for range_kata in [self.keywords["jerawat"]] for kata in range_kata):
            return "Kombinasi (Combination Skin)"
        elif any(kata in text for range_kata in [self.keywords["flek_hitam"]] for kata in range_kata):
            return "Kering (Dry Skin)"
        elif any(kata in text for range_kata in [self.keywords["skin_barrier"]] for kata in range_kata):
            return "Sensitif (Sensitive Skin)"
        else:
            return "Normal (Normal Skin)"