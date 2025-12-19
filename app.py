import streamlit as st
import time
import math
import pandas as pd

# Global counter untuk menghitung operasi/panggilan rekursif
# Note: Dalam lingkungan multi-threaded atau multi-user Streamlit, ini harus di-reset per sesi.
# Untuk demo sederhana ini, kita akan mengembalikannya dalam fungsi.

# --- 1. Implementasi Algoritma ---

def check_prime_iterative(n):
    """Cek Bilangan Prima (Iteratif)"""
    count = 0
    if n <= 1:
        return False, count
    if n <= 3:
        return True, count

    limit = int(math.sqrt(n))
    for i in range(2, limit + 1):
        count += 1
        if n % i == 0:
            return False, count
    return True, count

def check_prime_recursive_helper(n, current_divisor, count):
    """Helper untuk Cek Bilangan Prima (Rekursif)"""
    count[0] += 1
    if n % current_divisor == 0:
        return False, count[0]
    
    if current_divisor * current_divisor > n:
        return True, count[0]
    
    # Panggilan rekursif
    return check_prime_recursive_helper(n, current_divisor + 1, count)

def check_prime_recursive(n):
    """Cek Bilangan Prima (Rekursif)"""
    count = [0]  # Menggunakan list/mutable untuk menghitung dalam rekursi
    if n <= 1:
        return False, count[0]
    if n <= 3:
        return True, count[0]
    
    # Batasan keamanan rekursi Python
    if n > 1000000:
        return f"Error: Angka terlalu besar ({n}) untuk rekursi yang efisien.", count[0]

    try:
        return check_prime_recursive_helper(n, 2, count)
    except RecursionError:
        return "Error: Stack Overflow. Angka terlalu besar.", count[0]

def find_factors_iterative(n):
    """Faktorisasi Prima (Iteratif)"""
    count = 0
    factors = []
    temp_n = n
    d = 2

    while temp_n % 2 == 0:
        count += 1
        factors.append(2)
        temp_n //= 2

    d = 3
    while d * d <= temp_n:
        count += 1 # Menghitung loop luar
        while temp_n % d == 0:
            count += 1 # Menghitung loop dalam
            factors.append(d)
            temp_n //= d
        d += 2
    
    if temp_n > 1:
        factors.append(temp_n)
    
    return factors, count

def find_factors_recursive_helper(n, d, factors, count):
    """Helper untuk Faktorisasi Prima (Rekursif)"""
    count[0] += 1

    if n == 1:
        return factors, count[0]

    # Basis Rekursif
    if d * d > n:
        factors.append(n)
        return factors, count[0]

    # Kasus 1: d adalah faktor
    if n % d == 0:
        factors.append(d)
        return find_factors_recursive_helper(n // d, d, factors, count)
    
    # Kasus 2: Lanjut ke pembagi berikutnya
    return find_factors_recursive_helper(n, d + 1, factors, count)

def find_factors_recursive(n):
    """Faktorisasi Prima (Rekursif)"""
    count = [0]
    if n <= 1:
        return [], count[0]

    # Batasan keamanan rekursi Python
    if n > 1000000:
        return f"Error: Angka terlalu besar ({n}) untuk rekursi yang efisien.", count[0]

    try:
        return find_factors_recursive_helper(n, 2, [], count)
    except RecursionError:
        return "Error: Stack Overflow. Angka terlalu besar.", count[0]


# --- 2. Fungsi Analisis Utama ---

def run_analysis(N, func_type):
    """Menjalankan algoritma dan mengukur waktu eksekusi"""
    results = {}

    # --- Analisis Iteratif ---
    start_time_i = time.perf_counter()
    if func_type == 'isPrime':
        result, count = check_prime_iterative(N)
        output = f"{N} adalah Bilangan Prima" if result is True else f"{N} BUKAN Bilangan Prima" if result is False else result
    else: # primeFactors
        result, count = find_factors_iterative(N)
        output = " x ".join(map(str, result)) if isinstance(result, list) else result
    
    end_time_i = time.perf_counter()
    time_i = (end_time_i - start_time_i) * 1_000_000  # Mikrodetik (µs)
    results['Iterative'] = {'Waktu (µs)': time_i, 'Operasi/Panggilan': count, 'Hasil': output}


    # --- Analisis Rekursif ---
    start_time_r = time.perf_counter()
    if func_type == 'isPrime':
        result, count = check_prime_recursive(N)
        output = f"{N} adalah Bilangan Prima" if result is True else f"{N} BUKAN Bilangan Prima" if result is False else result
    else: # primeFactors
        result, count = find_factors_recursive(N)
        output = " x ".join(map(str, result)) if isinstance(result, list) else result

    end_time_r = time.perf_counter()
    time_r = (end_time_r - start_time_r) * 1_000_000  # Mikrodetik (µs)
    results['Recursive'] = {'Waktu (µs)': time_r, 'Operasi/Panggilan': count, 'Hasil': output}

    return results

# --- 3. Antarmuka Streamlit (UI) ---

st.set_page_config(
    page_title="Analisis Algoritma Prima", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🔬 Analisis Efisiensi Algoritma Prima (Python Streamlit)")
st.markdown("Aplikasi untuk membandingkan kinerja (waktu eksekusi dan jumlah operasi) antara algoritma Iteratif dan Rekursif.")

# Input Samping
with st.sidebar:
    st.header("Konfigurasi Input")
    try:
        N = st.number_input(
            "Masukkan Angka Positif (N):",
            min_value=1,
            value=100003,
            step=1,
            format="%d"
        )
    except Exception:
         st.error("Masukkan angka positif yang valid.")
         st.stop()
         
    # Batasan untuk Rekursif
    if N > 10**6:
        st.warning("Angka sangat besar! Algoritma Rekursif mungkin akan gagal (Stack Overflow).")
        
    st.header("Pilih Analisis")
    analysis_type = st.radio(
        "Pilih Jenis Tugas:",
        ('isPrime', 'primeFactors'),
        captions=['Cek apakah N bilangan prima?', 'Temukan faktor-faktor prima dari N.']
    )
    
    if st.button("Jalankan Analisis", type="primary"):
        st.session_state['run_flag'] = True
    else:
        # Menjamin tombol run harus ditekan
        if 'run_flag' not in st.session_state:
            st.session_state['run_flag'] = False

# Hanya jalankan jika tombol ditekan atau pada inisialisasi awal untuk nilai default
if st.session_state.get('run_flag'):
    
    st.subheader(f"Hasil untuk N = {N:,} ({'Cek Prima' if analysis_type == 'isPrime' else 'Faktorisasi Prima'})")

    # Jalankan Analisis
    try:
        results = run_analysis(N, analysis_type)
    except Exception as e:
        st.error(f"Terjadi kesalahan saat menjalankan analisis: {e}")
        st.stop()


    # 4. Tampilkan Hasil dalam Tabel (DataFrame)
    
    results_df = pd.DataFrame(results).T
    
    # Format kolom agar lebih mudah dibaca
    results_df['Waktu (µs)'] = results_df['Waktu (µs)'].apply(lambda x: f"{x:,.2f} µs")
    results_df['Operasi/Panggilan'] = results_df['Operasi/Panggilan'].apply(lambda x: f"{x:,.0f}")
    
    st.dataframe(results_df, use_container_width=True)

    # 5. Tampilkan Grafik Running Time
    st.subheader("Visualisasi Waktu Eksekusi (µs)")

    # Data untuk grafik
    chart_data = pd.DataFrame({
        'Metode': ['Iteratif', 'Rekursif'],
        'Waktu (µs)': [
            results['Iterative']['Waktu (µs)'] / 1000 if "Error" in results['Iterative']['Hasil'] else results['Iterative']['Waktu (µs)'], # Jika error, beri waktu 0 atau skala kecil
            results['Recursive']['Waktu (µs)'] / 1000 if "Error" in results['Recursive']['Hasil'] else results['Recursive']['Waktu (µs)']
        ]
    })
    
    # Pencegahan jika waktu eksekusi 0 atau sangat kecil, yang mungkin membuat chart.js kesulitan
    if chart_data['Waktu (µs)'].max() < 1:
         st.info("Waktu eksekusi sangat kecil (< 1 µs). Grafik mungkin tidak terlihat jelas.")
    
    # Membuat Bar Chart menggunakan Plotly bawaan Streamlit
    st.bar_chart(chart_data.set_index('Metode'), color="#2ecc71")
    
    st.markdown("""
        ---
        **Analisis:**
        * **Iteratif (Operasi):** Menghitung jumlah perulangan/pembagian yang terjadi.
        * **Rekursif (Panggilan):** Menghitung jumlah total panggilan fungsi rekursif.
        * **Waktu (µs):** Diukur menggunakan `time.perf_counter()` dan dikonversi ke mikrodetik ($\mu\text{s}$).
        """)