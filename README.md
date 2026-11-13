# Proyek Analisis Data: Bike Sharing Dataset 🚲

Proyek ini disusun sebagai syarat kelulusan kelas **Belajar Analisis Data dengan Python** di Dicoding. Tujuan utama dari proyek ini adalah untuk mengeksplorasi, menganalisis, serta memvisualisasikan pola penyewaan sepeda berdasarkan kondisi cuaca dan perilaku pengguna (*casual* vs *registered*) dari tahun 2011 hingga 2012, yang kemudian disajikan dalam bentuk *dashboard* interaktif menggunakan **Streamlit**.

---

## 👤 Informasi Penyusun
* **Nama:** Muhammad Riza Alfarizi
* **Email:** rizaalfa1275@gmail.com
* **ID Dicoding:** rizaaacute

---

## 🎯 Pertanyaan Bisnis
Analisis dalam proyek ini berfokus pada tiga pertanyaan bisnis utama yang dirumuskan menggunakan kerangka kerja *SMART*:
1. **Sensitivitas Suhu Ekstrem:** Bagaimana perbandingan tingkat sensitivitas antara pengguna kasual (*casual*) dan pengguna terdaftar (*registered*) terhadap lonjakan suhu lingkungan (*normalized temperature* > 0.7) sepanjang tahun 2012?
2. **Dampak Angin pada Jam Sibuk:** Seberapa besar penurunan persentase rata-rata penyewaan sepeda pada jam-jam sibuk pagi (pukul 07.00 - 09.00) di hari kerja (*workingday = 1*) ketika kecepatan angin melampaui batas normal (*windspeed* > 0.3) selama periode 2011–2012?
3. **Perilaku Pengguna Akhir Pekan Saat Cuaca Buruk:** Bagaimana pola penurunan volume penyewaan antara pengguna kasual dan terdaftar saat kondisi cuaca memburuk dari cerah (*Clear/Partly Cloudy*) ke kondisi berawan/kabut (*Mist/Cloudy*) atau hujan ringan (*Light Rain/Snow*) khusus pada hari libur atau akhir pekan (*workingday = 0*)?

---

## 💡 Ringkasan Temuan Utama (*Key Insights*)
* **Pengaruh Suhu Lingkungan:** Lonjakan suhu hangat (*temp* > 0.7) di tahun 2012 mendorong peningkatan signifikan pada volume penyewaan sepeda, yang didominasi oleh pengguna *registered* (pekerja/pelajar rutin).
* **Hambatan Kecepatan Angin:** Pada jam sibuk pagi hari kerja, kecepatan angin di atas 0.3 menekan minat bersepeda para *commuter*, membuat kurva penyewaan berada konsisten di bawah rata-rata kondisi angin normal.
* **Sensitivitas Cuaca pada Akhir Pekan:** Pengguna *casual* (wisatawan/rekreasi) jauh lebih sensitif terhadap cuaca buruk dibandingkan pengguna *registered*, dengan penurunan volume penyewaan yang sangat tajam saat cuaca berubah dari cerah menjadi hujan ringan.

---

## 📁 Struktur Direktori Proyek
```text
submission/
├── dashboard/
│   ├── main_data.csv       # Dataset bersih hasil proses Data Wrangling untuk dashboard
│   └── dashboard.py        # Kode utama aplikasi dashboard interaktif Streamlit
├── data/
│   ├── day.csv             # Dataset mentah penyewaan sepeda harian
│   └── hour.csv            # Dataset mentah penyewaan sepeda per jam
├── notebook.ipynb          # Jupyter/Colab Notebook berisi seluruh tahapan analisis data
├── README.md               # Dokumentasi proyek dan panduan menjalankan aplikasi
├── requirements.txt        # Daftar library Python yang dibutuhkan
└── url.txt                 # Tautan menuju dashboard yang telah di-deploy ke Streamlit Cloud
```

---

## 🛠️ Panduan Instalasi & Menjalankan Dashboard Secara Lokal

Ikuti langkah-langkah berikut untuk menjalankan *dashboard* di komputer lokal Anda:

1. **Unduh atau Clone Repositori**
   Pastikan seluruh berkas berada dalam struktur direktori yang sesuai seperti pada bagian di atas.

2. **Buka Terminal / Command Prompt**
   Arahkan direktori aktif ke folder utama proyek `submission/`.

3. **Buat Virtual Environment (Opsional namun Disarankan)**
   ```bash
   python -m venv venv
   # Aktivasi di Windows:
   venv\Scripts\activate
   # Aktivasi di macOS/Linux:
   source venv/bin/activate
   ```

4. **Instal Semua Library yang Dibutuhkan**
   Jalankan perintah berikut untuk menginstal seluruh dependensi yang tercatat di `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

5. **Jalankan Aplikasi Dashboard Streamlit**
   Masuk ke dalam folder `dashboard` dan jalankan perintah `streamlit run`:
   ```bash
   cd dashboard
   streamlit run dashboard.py
   ```
   Setelah perintah dijalankan, *browser* akan otomatis terbuka dan menampilkan *dashboard* pada alamat lokal (biasanya `http://localhost:8501`).

---

## 🌐 Akses Dashboard Online (Streamlit Cloud)
Dashboard interaktif ini juga telah di-*deploy* secara daring menggunakan **Streamlit Community Cloud**. Anda dapat mengakses tautan langsungnya melalui berkas **`url.txt`** yang disertakan di dalam folder proyek ini.

---

## 📊 Sumber Dataset
Dataset yang digunakan dalam proyek ini adalah **Bike Sharing Dataset** yang bersumber dari sistem penyewaan sepeda Capital Bikeshare di Washington D.C., Amerika Serikat (periode tahun 2011–2012), tersedia secara publik melalui UCI Machine Learning Repository.