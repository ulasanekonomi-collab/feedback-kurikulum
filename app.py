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
