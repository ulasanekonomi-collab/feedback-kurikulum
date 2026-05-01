def map_status_to_perspective(status):
    # Mapping otomatis dari Status ke Perspektif
    mapping = {
        "Dosen Internal": "Akademisi & Praktisi",
        "Dosen Luar/Pakar": "Akademisi & Praktisi",
        "Pimpinan Kampus": "Pengembang Sistem",
        "Alumni": "Pengguna & Stakeholder",
        "Stakeholder/Pengguna Lulusan": "Pengguna & Stakeholder",
        "Mahasiswa Aktif": "Pengguna & Stakeholder"
    }
    return mapping.get(status, "Pengguna & Stakeholder")

# Contoh cara kerja saat data masuk
status_responden = "Pimpinan Kampus"
perspektif_hasil_mapping = map_status_to_perspective(status_responden)

print(f"Status: {status_responden} -> Bobot Attention: {perspektif_hasil_mapping}")
def calculate_attention_score(row):
    # 1. Map Bobot Perspektif (P)
    perspektif_weights = {
        "Pengembang Sistem": 3,
        "Akademisi & Praktisi": 2,
        "Pengguna & Stakeholder": 1
    }
    p_score = perspektif_weights.get(row['perspektif'], 1)
    
    # 2. Hitung Intensitas (I) berdasarkan panjang teks Solution
    # Semakin detail solusinya, semakin tinggi bobotnya
    i_score = len(str(row['solution'])) / 100  # Normalisasi sederhana
    
    # 3. Urgensi dari User (U)
    u_score = row['urgency_user']
    
    # 4. Keyword Boost (Bonus jika ada kata kunci krusial)
    bonus = 0
    keywords = ["ketidaklengkapan", "kontradiksi", "regulasi", "mendasar"]
    if any(word in row['critique'].lower() for word in keywords):
        bonus = 2
        
    # Rumus Final Attention Score
    total_score = (p_score * i_score) + u_score + bonus
    return round(total_score, 2)
