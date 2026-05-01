import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Koreksi Kurikulum EP", layout="wide", initial_sidebar_state="expanded")

# 2. Inisialisasi Session State (Penyimpanan Data)
if 'data_usulan' not in st.session_state:
    st.session_state.data_usulan = [
        {
            "nama": "Sistem",
            "status": "Admin",
            "perspektif": "Pengembang Sistem",
            "area": "Area B: Struktur",
            "issues": "Contoh: Bab V",
            "critique": "Ketidaklengkapan materi digital.",
            "solution": "Tambahkan modul literasi data.",
            "urgency_user": 3
        }
    ]

# 3. Fungsi Logika (Mapping, Scoring, & KKO)
def map_status_to_perspective(status):
    mapping = {
        "Dosen Internal": "Akademisi & Praktisi",
        "Pimpinan Kampus": "Pengembang Sistem",
        "Alumni": "Pengguna & Stakeholder",
        "Stakeholder": "Pengguna & Stakeholder"
    }
    return mapping.get(status, "Pengguna & Stakeholder")

def calculate_attention_score(row):
    weights = {"Pengembang Sistem": 3, "Akademisi & Praktisi": 2, "Pengguna & Stakeholder": 1}
    p_score = weights.get(row['perspektif'], 1)
    i_score = len(str(row['solution'])) / 100
    u_score = row['urgency_user']
    bonus = 2 if any(word in str(row['critique']).lower() for word in ["ketidaklengkapan", "kontradiksi", "regulasi"]) else 0
    return round((p_score * i_score) + u_score + bonus, 2)

def suggest_kko(critique):
    crit = str(critique).lower()
    if any(word in crit for word in ["kurang", "tidak ada", "ketidaklengkapan"]):
        return "TAMBAHKAN/LENGKAPI"
    elif any(word in crit for word in ["tumpang tindih", "kontradiksi"]):
        return "SELARASKAN/SINKRONKAN"
    elif any(word in crit for word in ["kuno", "relevansi", "modern"]):
        return "MUTAKHIRKAN"
    elif any(word in crit for word in ["berat", "terlalu banyak", "sks"]):
        return "SEDERHANAKAN"
    return "REVISI"

# 4. Interface Form Aspirasi
st.title("Penyempurnaan Draft 7 Kurikulum EP Unisba")
st.markdown("### Landasan: Pedoman OBE 2024 & William Spady")

st.header("Form Aspirasi")
c1, c2 = st.columns(2)
with c1:
    nama_in = st.text_input("Nama")
    status_in = st.selectbox("Status", ["Dosen Internal", "Pimpinan Kampus", "Alumni", "Stakeholder"])
    area_in = st.selectbox("Area Fokus", ["Area A: Fondasi", "Area B: Struktur", "Area C: Proses", "Area D: Evaluasi"])
with c2:
    issue_in = st.text_input("Issues (Halaman/Bab)")
    urgency_in = st.slider("Tingkat Urgensi", 1, 5, 3)

critique_in = st.text_area("Critique (Analisis Masalah)")
solution_in = st.text_area("Solution (Usulan Perbaikan)")

if st.button("Kirim Usulan", use_container_width=True):
    if nama_in and solution_in:
        new_entry = {
            "nama": nama_in,
            "status": status_in,
            "perspektif": map_status_to_perspective(status_in),
            "area": area_in,
            "issues": issue_in,
            "critique": critique_in,
            "solution": solution_in,
            "urgency_user": urgency_in
        }
        st.session_state.data_usulan.append(new_entry)
        st.success(f"Berhasil! Usulan dari {nama_in} telah masuk.")
    else:
        st.warning("Nama dan Solusi wajib diisi.")

st.divider()

# 5. Dashboard Analisis (Deductive Logical View)
st.subheader("Daftar Usulan Berdasarkan Bobot Perhatian (Attention)")

if st.session_state.data_usulan:
    df = pd.DataFrame(st.session_state.data_usulan)
    
    # Proses Skor dan KKO secara kolektif
    df['attention_score'] = df.apply(calculate_attention_score, axis=1)
    df['rekomendasi_kko'] = df['critique'].apply(suggest_kko)
    
    # Urutkan berdasarkan Skor Tertinggi
    df_sorted = df.sort_values(by='attention_score', ascending=False)
    
    # Tampilkan Tabel Terintegrasi
    st.dataframe(
        df_sorted[['attention_score', 'rekomendasi_kko', 'nama', 'area', 'issues', 'solution']], 
        use_container_width=True
    )

    # Opsi Download Data
    csv = df_sorted.to_csv(index=False).encode('utf-8')
    st.download_button("Unduh Hasil Analisis (CSV)", csv, "rekap_usulan_ep.csv", "text/csv")
