import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Mengatur gaya visualisasi Seaborn
sns.set_style("whitegrid")

# Fungsi untuk memuat data secara aman (baik dijalankan dari root maupun folder dashboard/)
@st.cache_data
def load_data():
    possible_paths = [
        "main_data.csv",
        "dashboard/main_data.csv",
        os.path.join(os.path.dirname(__file__), "main_data.csv")
    ]
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            df["dteday"] = pd.to_datetime(df["dteday"])
            return df
    raise FileNotFoundError("File main_data.csv tidak ditemukan. Pastikan file berada di folder yang sama dengan dashboard.py.")

hour_df = load_data()

# Fungsi untuk membentuk agregasi harian dari main_data.csv
def create_daily_df(df):
    daily_df = df.groupby("dteday", as_index=False).agg({
        "season": "first",
        "yr": "first",
        "mnth": "first",
        "holiday": "first",
        "weekday": "first",
        "workingday": "first",
        "weathersit": lambda x: x.mode()[0],
        "temp": "mean",
        "atemp": "mean",
        "hum": "mean",
        "windspeed": "mean",
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return daily_df

# ==============================================================================
# SIDEBAR FILTER INTERAKTIF
# ==============================================================================
with st.sidebar:
    # Menambahkan logo Dicoding tepat di atas judul Bike Sharing
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.title("🚲 Bike Sharing")
    st.markdown("Filter rentang waktu dan kondisi musim di bawah ini untuk mengeksplorasi data penyewaan sepeda.")

    min_date = hour_df["dteday"].min().date()
    max_date = hour_df["dteday"].max().date()

    date_range = st.date_input(
        label="Rentang Tanggal",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0] if isinstance(date_range, (list, tuple)) else date_range

    selected_seasons = st.multiselect(
        label="Pilih Musim (Season)",
        options=hour_df["season"].unique().tolist(),
        default=hour_df["season"].unique().tolist()
    )

    st.markdown("---")
    st.caption("Proyek Analisis Data — Dicoding Submission")

# Terapkan filter pada data
filtered_hour_df = hour_df[
    (hour_df["dteday"].dt.date >= start_date) &
    (hour_df["dteday"].dt.date <= end_date) &
    (hour_df["season"].isin(selected_seasons))
].copy()

if filtered_hour_df.empty:
    st.warning("Data kosong untuk kombinasi filter yang dipilih. Silakan sesuaikan rentang tanggal atau musim di sidebar.")
    st.stop()

filtered_day_df = create_daily_df(filtered_hour_df)

# ==============================================================================
# HEADER & RINGKASAN METRIK UTAMA (KPI)
# ==============================================================================
st.title("📊 Dashboard Analisis Penyewaan Sepeda (Bike Sharing)")
st.markdown(
    "Dashboard ini menyajikan hasil analisis pengaruh faktor lingkungan (suhu, kecepatan angin, dan kondisi cuaca) "
    "terhadap perilaku pengguna kasual (*casual*) dan terdaftar (*registered*)."
)

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
with col_kpi1:
    st.metric("Total Penyewaan", f"{int(filtered_day_df['cnt'].sum()):,}")
with col_kpi2:
    st.metric("Pengguna Registered", f"{int(filtered_day_df['registered'].sum()):,}")
with col_kpi3:
    st.metric("Pengguna Casual", f"{int(filtered_day_df['casual'].sum()):,}")
with col_kpi4:
    st.metric("Rata-rata Harian", f"{filtered_day_df['cnt'].mean():,.0f}")

st.markdown("---")

# ==============================================================================
# TAB NAVIGASI AGAR TAMPILAN RAPI & TERTATA
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "1️⃣ Pengaruh Suhu (2012)",
    "2️⃣ Kecepatan Angin Jam Sibuk",
    "3️⃣ Cuaca di Akhir Pekan",
    "4️⃣ Matriks Korelasi"
])

# ------------------------------------------------------------------------------
# TAB 1: PERTANYAAN 1
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("1. Sensitivitas Pengguna Casual vs Registered Terhadap Suhu Tinggi (> 0.7)")
    st.markdown(
        "**Pertanyaan Bisnis:** *Bagaimana perbandingan tingkat sensitivitas antara pengguna kasual (casual) dan "
        "pengguna terdaftar (registered) terhadap lonjakan suhu lingkungan (normalized temperature > 0.7) sepanjang tahun 2012?*"
    )

    df_2012 = filtered_day_df[filtered_day_df["yr"] == 1].copy()

    if df_2012.empty:
        st.info("Data tahun 2012 tidak tersedia pada rentang tanggal yang dipilih. Silakan perluas filter tanggal hingga tahun 2012.")
    else:
        df_2012["temp_category"] = df_2012["temp"].apply(
            lambda x: "Suhu Tinggi (> 0.7)" if x > 0.7 else "Suhu Normal/Sejuk"
        )
        temp_user_df = df_2012.groupby("temp_category")[["casual", "registered"]].mean().reset_index()
        temp_user_melted = pd.melt(
            temp_user_df,
            id_vars=["temp_category"],
            value_vars=["casual", "registered"],
            var_name="user_type",
            value_name="average_count"
        )

        col_chart1, col_info1 = st.columns([2.2, 1])
        with col_chart1:
            fig1, ax1 = plt.subplots(figsize=(9, 5))
            sns.barplot(
                x="temp_category",
                y="average_count",
                hue="user_type",
                data=temp_user_melted,
                palette="viridis",
                ax=ax1
            )
            ax1.set_title("Perbandingan Rata-rata Penyewa (Casual vs Registered) Berdasarkan Kondisi Suhu (2012)", fontsize=11, fontweight="bold", pad=12)
            ax1.set_xlabel("Kategori Suhu", fontsize=10)
            ax1.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=10)
            handles, _ = ax1.get_legend_handles_labels()
            ax1.legend(handles=handles, title="Tipe Pengguna", labels=["Casual", "Registered"])
            plt.tight_layout()
            st.pyplot(fig1)
            plt.close(fig1)

        with col_info1:
            st.markdown("#### 💡 Insight Utama")
            st.info(
                "Lonjakan suhu tinggi (*temp > 0.7*) di tahun 2012 justru meningkatkan rata-rata penyewaan sepeda "
                "pada kedua kelompok pengguna. Pengguna **registered** mencatat lonjakan volume rata-rata yang jauh lebih "
                "tinggi dibandingkan pengguna **casual**."
            )
            st.dataframe(
                temp_user_df.rename(columns={
                    "temp_category": "Kategori Suhu",
                    "casual": "Rata-rata Casual",
                    "registered": "Rata-rata Registered"
                }).style.format({"Rata-rata Casual": "{:.1f}", "Rata-rata Registered": "{:.1f}"}),
                use_container_width=True,
                hide_index=True
            )

# ------------------------------------------------------------------------------
# TAB 2: PERTANYAAN 2
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("2. Dampak Kecepatan Angin (> 0.3) pada Jam Sibuk Pagi Hari Kerja")
    st.markdown(
        "**Pertanyaan Bisnis:** *Seberapa besar penurunan persentase rata-rata penyewaan sepeda pada jam-jam sibuk pagi "
        "(pukul 07.00 - 09.00) di hari kerja (workingday = 1) ketika kecepatan angin melampaui batas normal (windspeed > 0.3)?*"
    )

    morning_rush = filtered_hour_df[
        (filtered_hour_df["workingday"] == 1) & (filtered_hour_df["hr"].isin([7, 8, 9]))
    ].copy()

    if morning_rush.empty:
        st.info("Data jam sibuk pagi hari kerja tidak tersedia untuk filter yang dipilih.")
    else:
        morning_rush["wind_category"] = morning_rush["windspeed"].apply(
            lambda x: "Angin Kencang (> 0.3)" if x > 0.3 else "Angin Normal (<= 0.3)"
        )
        wind_rush_df = morning_rush.groupby(["hr", "wind_category"])["cnt"].mean().reset_index()

        # Hitung rata-rata keseluruhan & persentase penurunan
        avg_normal = morning_rush[morning_rush["windspeed"] <= 0.3]["cnt"].mean()
        avg_high = morning_rush[morning_rush["windspeed"] > 0.3]["cnt"].mean()

        col_chart2, col_info2 = st.columns([2.2, 1])
        with col_chart2:
            fig2, ax2 = plt.subplots(figsize=(9, 5))
            sns.lineplot(
                x="hr",
                y="cnt",
                hue="wind_category",
                data=wind_rush_df,
                marker="o",
                linewidth=2.5,
                palette="Set1",
                ax=ax2
            )
            ax2.set_title("Pola Penyewaan Sepeda Jam Sibuk Pagi (07.00 - 09.00) Berdasarkan Kecepatan Angin", fontsize=11, fontweight="bold", pad=12)
            ax2.set_xlabel("Jam (Hour)", fontsize=10)
            ax2.set_ylabel("Rata-rata Total Penyewaan (Cnt)", fontsize=10)
            ax2.set_xticks([7, 8, 9])
            ax2.set_xticklabels(["07:00", "08:00", "09:00"])
            ax2.legend(title="Kondisi Angin")
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close(fig2)

        with col_info2:
            st.markdown("#### 💡 Insight Utama")
            if pd.notna(avg_normal) and pd.notna(avg_high) and avg_normal > 0:
                drop_pct = ((avg_normal - avg_high) / avg_normal) * 100
                st.metric(
                    label="Penurunan Rata-rata (Angin Kencang)",
                    value=f"{avg_high:.1f} / jam",
                    delta=f"-{drop_pct:.1f}% vs Angin Normal"
                )
            st.info(
                "Pada jam berangkat kerja/sekolah (puncak pada pukul 08:00), kondisi angin kencang (*windspeed > 0.3*) "
                "secara konsisten menekan minat bersepeda dibandingkan saat kecepatan angin normal."
            )

# ------------------------------------------------------------------------------
# TAB 3: PERTANYAAN 3
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("3. Pola Penurunan Penyewaan Saat Cuaca Memburuk di Akhir Pekan / Hari Libur")
    st.markdown(
        "**Pertanyaan Bisnis:** *Bagaimana pola penurunan volume penyewaan antara pengguna kasual dan terdaftar saat kondisi "
        "cuaca memburuk dari cerah ke berawan/kabut atau hujan ringan khusus pada hari libur atau akhir pekan (workingday = 0)?*"
    )

    weekend_df = filtered_day_df[filtered_day_df["workingday"] == 0].copy()

    if weekend_df.empty:
        st.info("Data akhir pekan / hari libur tidak tersedia untuk filter yang dipilih.")
    else:
        weather_order = [
            w for w in ["Clear/Partly Cloudy", "Mist/Cloudy", "Light Rain/Snow", "Severe Weather"]
            if w in weekend_df["weathersit"].unique()
        ]
        weather_weekend_df = (
            weekend_df.groupby("weathersit")[["casual", "registered"]]
            .mean()
            .reindex(weather_order)
            .reset_index()
        )
        weather_melted = pd.melt(
            weather_weekend_df,
            id_vars=["weathersit"],
            value_vars=["casual", "registered"],
            var_name="user_type",
            value_name="average_count"
        )

        col_chart3, col_info3 = st.columns([2.2, 1])
        with col_chart3:
            fig3, ax3 = plt.subplots(figsize=(9, 5))
            sns.barplot(
                x="weathersit",
                y="average_count",
                hue="user_type",
                data=weather_melted,
                palette="muted",
                ax=ax3
            )
            ax3.set_title("Rata-rata Penyewaan saat Akhir Pekan / Hari Libur Berdasarkan Kondisi Cuaca", fontsize=11, fontweight="bold", pad=12)
            ax3.set_xlabel("Kondisi Cuaca (Weather Situation)", fontsize=10)
            ax3.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=10)
            handles3, _ = ax3.get_legend_handles_labels()
            ax3.legend(handles=handles3, title="Tipe Pengguna", labels=["Casual", "Registered"])
            plt.tight_layout()
            st.pyplot(fig3)
            plt.close(fig3)

        with col_info3:
            st.markdown("#### 💡 Insight Utama")
            st.info(
                "Saat cuaca berubah dari cerah ke hujan ringan pada akhir pekan atau hari libur, pengguna **casual** "
                "mengalami penurunan persentase yang jauh lebih drastis dibandingkan pengguna **registered** karena "
                "perjalanan mereka umumnya bersifat rekreasi."
            )
            st.dataframe(
                weather_weekend_df.rename(columns={
                    "weathersit": "Kondisi Cuaca",
                    "casual": "Rata-rata Casual",
                    "registered": "Rata-rata Registered"
                }).style.format({"Rata-rata Casual": "{:.1f}", "Rata-rata Registered": "{:.1f}"}),
                use_container_width=True,
                hide_index=True
            )

# ------------------------------------------------------------------------------
# TAB 4: ANALISIS LANJUTAN (MATRIKS KORELASI)
# ------------------------------------------------------------------------------
with tab4:
    st.subheader("4. Analisis Lanjutan: Matriks Korelasi Variabel Lingkungan & Penyewaan")
    st.markdown(
        "Visualisasi *heatmap* berikut memperlihatkan kekuatan hubungan linear antara variabel cuaca/lingkungan "
        "(`temp`, `atemp`, `hum`, `windspeed`) dengan jumlah penyewaan sepeda (`casual`, `registered`, `cnt`)."
    )

    col_chart4, col_info4 = st.columns([2, 1])
    with col_chart4:
        selected_cols = ["temp", "atemp", "hum", "windspeed", "casual", "registered", "cnt"]
        correlation_matrix = filtered_day_df[selected_cols].corr()

        fig4, ax4 = plt.subplots(figsize=(8, 5.5))
        sns.heatmap(
            correlation_matrix,
            annot=True,
            cmap="coolwarm",
            fmt=".2f",
            linewidths=0.5,
            ax=ax4
        )
        ax4.set_title("Matriks Korelasi Variabel Lingkungan dan Penyewaan Sepeda", fontsize=11, fontweight="bold", pad=12)
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close(fig4)

    with col_info4:
        st.markdown("#### 💡 Insight Korelasi")
        st.info("""
- **Suhu (`temp` & `atemp`):** Memiliki korelasi positif terkuat (~0.63) terhadap total penyewaan (`cnt`).
- **Kelembapan & Angin (`hum` & `windspeed`):** Memiliki korelasi negatif, yang menandakan udara terlalu lembap atau berangin cenderung menurunkan jumlah penyewa.
- **Dominasi Pengguna (`registered`):** Berkorelasi sangat tinggi (0.95) dengan total penyewaan harian.
""")

# ==============================================================================
# KESIMPULAN & REKOMENDASI AKSI
# ==============================================================================
st.markdown("---")
with st.expander("📌 Ringkasan Kesimpulan & Rekomendasi Strategis", expanded=True):
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("""
**Kesimpulan Utama:**
1. **Suhu Tinggi (2012):** Lonjakan suhu (*temp > 0.7*) meningkatkan rata-rata peminjaman, terutama didominasi oleh pengguna *registered*.
2. **Angin Kencang Pagi Hari:** Kecepatan angin *windspeed > 0.3* pada jam sibuk pagi (07.00–09.00) menekan rata-rata penyewaan *commuter*.
3. **Cuaca Buruk Akhir Pekan:** Hujan ringan pada hari libur menurunkan volume pengguna *casual* jauh lebih tajam dibanding *registered*.
""")
    with col_c2:
        st.markdown("""
**Rekomendasi Action Item:**
- **Alokasi Armada Dinamis:** Tingkatkan ketersediaan unit sepeda pada hari bersuhu hangat serta perkuat perawatan armada saat prakiraan angin kencang/hujan.
- **Segmentasi Promosi:** Perkuat program loyalitas bagi pengguna *registered* di hari kerja, dan tawarkan promo khusus akhir pekan cerah untuk menarik pengguna *casual*.
""")
