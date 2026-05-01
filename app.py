import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Koreksi Kurikulum EP", layout="wide", initial_sidebar_state="expanded")

# 2. Inisialisasi Session State (Wadah Penyimpanan Data)
if 'data_usulan' not in st.session_state:
    # Data awal/pancingan agar tabel tidak kosong
    st.session_state.data_usulan = [
        {
            "nama": "Sistem",
            "status": "Admin",
            "perspektif": "Pengembang Sistem",
            "area": "Area B: Struktur",
            "issues": "Contoh: Bab V",
            "critique": "Contoh kritik...",
            "solution": "Contoh solusi...",
            "urgency_user": 3
        }
    ]

# 3. Fungsi Logika (Mapping & Scoring)
def map_status_to_perspective(status):
    mapping = {
        "Dosen Internal": "Akademisi & Praktisi",
        "Pimpinan Kampus": "Pengembang Sistem",
        "Alumni": "Pengguna & Stakeholder",
        "Stakeholder": "Pengguna & Stakeholder"
    }
    return mapping.get(status, "Pengguna & Stakeholder")

def calculate_attention_score(row):
    perspektif_weights = {"Pengembang Sistem": 3, "Akademisi & Praktisi": 2, "Pengguna & Stakeholder": 1}
    p_score = perspektif_weights.get(row['perspektif'], 1)
    i_score = len(str(row['solution'])) / 100
    u_score = row['urgency_user']
    bonus = 2 if any(word in str(row['critique']).lower() for word in ["ketidaklengkapan", "kontradiksi", "regulasi"]) else 0
    return round((p_score * i_score) + u_score + bonus, 2)

# 4. Tampilan Interface
st.title("Penyempurnaan Draft 7 Kurikulum EP Unisba")

st.header("Form Aspirasi")
col1, col2 = st.columns(2)

with col1:
    nama_input = st.text_input("Nama")
    status_input = st.selectbox("Status", ["Dosen Internal", "Pimpinan Kampus", "Alumni", "Stakeholder"])
    area_input = st.selectbox("Area Fokus", ["Area A: Fondasi", "Area B: Struktur", "Area C: Proses", "Area D: Evaluasi"])

with col2:
    issue_input = st.text_input("Issues (Halaman/Bab)")
    urgency_input = st.slider("Tingkat Urgensi", 1, 5, 3)

critique_input = st.text_area("Critique (Analisis)")
solution_input = st.text_area("Solution (Usulan Konkret)")

# TOMBOL KIRIM (Proses Koneksi Data)
if st.button("Kirim Usulan", use_container_width=True):
    if nama_input and solution_input: # Validasi sederhana
        # Buat dictionary data baru
        new_data = {
            "nama": nama_input,
            "status": status_input,
            "perspektif": map_status_to_perspective(status_input),
            "area": area_input,
            "issues": issue_input,
            "critique": critique_input,
            "solution": solution_input,
            "urgency_user": urgency_input
        }
        # Masukkan ke dalam session_state
        st.session_state.data_usulan.append(new_data)
        st.success(f"Terima kasih {nama_input}, usulan Anda telah terkoneksi ke sistem!")
    else:
        st.error("Mohon isi Nama dan Solution terlebih dahulu.")

st.divider()

# 5. Dashboard (Menampilkan Data dari Session State)
st.subheader("Daftar Usulan Berdasarkan Bobot Perhatian (Attention)")

if st.session_state.data_usulan:
    df = pd.DataFrame(st.session_state.data_usulan)
    df['attention_score'] = df.apply(calculate_attention_score, axis=1)
    df_sorted = df.sort_values(by='attention_score', ascending=False)
    
    # Menampilkan Tabel
    st.dataframe(df_sorted[['attention_score', 'nama', 'status', 'area', 'issues', 'solution']], use_container_width=True)

    # Opsi Download
    csv = df_sorted.to_csv(index=False).encode('utf-8')
    st.download_button("Unduh Rekap CSV", data=csv, file_name='rekap_usulan.csv', mime='text/csv')
