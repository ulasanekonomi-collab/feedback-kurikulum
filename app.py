import streamlit as st
import pandas as pd

# 1. JUDUL DAN PROLOG (Sesuai diskusi kita tadi)
st.set_page_config(page_title="Koreksi Kurikulum EP", layout="wide")
st.title("Penyempurnaan Draft 7 Kurikulum EP Unisba")
st.markdown("""
### Prolog: Transformasi Kurikulum Berbasis Standar dan Masa Depan
Penyusunan draf ini mengacu pada **Pedoman Kurikulum OBE Kemendiktisaintek 2024** dan filosofi **William Spady**. 
Kami mengundang Bapak/Ibu untuk memberikan 'Attention' pada area strategis demi kemaslahatan umat.
""")

# 2. DATA SIMULASI (Supaya tidak error 'data_usulan is not defined')
# Nantinya data ini bisa diambil dari database atau CSV
data_usulan = [
    {
        "nama": "Contoh User",
        "perspektif": "Pengembang Sistem",
        "area": "Area B: Struktur & Kompetensi",
        "issues": "Prasyarat mata kuliah",
        "critique": "Aya ketidaklengkapan dalam logika dasar.",
        "solution": "Tambahkan matkul prasyarat Python.",
        "urgency_user": 5
    }
]

# 3. FUNGSI LOGIKA (Attention Mechanism)
def map_status_to_perspective(status):
    mapping = {
        "Dosen Internal": "Akademisi & Praktisi",
        "Dosen Luar/Pakar": "Akademisi & Praktisi",
        "Pimpinan Kampus": "Pengembang Sistem",
        "Alumni": "Pengguna & Stakeholder",
        "Stakeholder/Pengguna Lulusan": "Pengguna & Stakeholder",
        "Mahasiswa Aktif": "Pengguna & Stakeholder"
    }
    return mapping.get(status, "Pengguna & Stakeholder")

def calculate_attention_score(row):
    perspektif_weights = {"Pengembang Sistem": 3, "Akademisi & Praktisi": 2, "Pengguna & Stakeholder": 1}
    p_score = perspektif_weights.get(row['perspektif'], 1)
    i_score = len(str(row['solution'])) / 100
    u_score = row['urgency_user']
    
    bonus = 2 if any(word in row['critique'].lower() for word in ["ketidaklengkapan", "kontradiksi", "regulasi"]) else 0
    return round((p_score * i_score) + u_score + bonus, 2)

# 4. FORM INPUT DI STREAMLIT (Tampilan untuk Responden)
with st.sidebar:
    st.header("Form Aspirasi")
    nama = st.text_input("Nama")
    status = st.selectbox("Status", ["Dosen Internal", "Pimpinan Kampus", "Alumni", "Stakeholder"])
    area = st.selectbox("Area Fokus", ["Area A: Fondasi", "Area B: Struktur", "Area C: Proses", "Area D: Evaluasi"])
    issue = st.text_input("Issues (Halaman/Bab)")
    critique = st.text_area("Critique (Analisis)")
    solution = st.text_area("Solution (Usulan Konkret)")
    urgency = st.slider("Tingkat Urgensi", 1, 5, 3)
    
    if st.button("Kirim Usulan"):
        # Logika simpan data (sementara masuk ke list)
        st.success("Usulan berhasil dikirim!")

# 5. DISPLAY DASHBOARD (Logika Deduktif - Ide Pokok di Atas)
st.subheader("Daftar Usulan Berdasarkan Bobot Perhatian (Attention)")
df = pd.DataFrame(data_usulan)
df['attention_score'] = df.apply(calculate_attention_score, axis=1)
df_sorted = df.sort_values(by='attention_score', ascending=False)

st.table(df_sorted[['attention_score', 'nama', 'area', 'issues', 'solution']])
