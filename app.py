import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Fish Growth Monitoring",
    page_icon="🐟",
    layout="wide"
)

FILE = "data_pertumbuhan.csv"

st.title("🐟 Fish Growth Monitoring")
st.caption("Sistem Monitoring Pertumbuhan Ikan Budidaya")

# Membaca data
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=[
        "Tanggal", "Jenis Ikan", "Jumlah",
        "Berat (gram)", "Panjang (cm)"
    ])

st.divider()

# Form input
st.header("📝 Input Data Pertumbuhan")

with st.form("form_ikan"):
    jenis = st.selectbox(
        "Jenis ikan",
        ["Lele", "Nila", "Gurame", "Bandeng", "Patin"]
    )

    tanggal = st.date_input("Tanggal pengukuran")

    jumlah = st.number_input(
        "Jumlah ikan",
        min_value=1,
        value=10
    )

    berat = st.number_input(
        "Berat rata-rata (gram)",
        min_value=0.1,
        value=100.0
    )

    panjang = st.number_input(
        "Panjang rata-rata (cm)",
        min_value=0.1,
        value=15.0
    )

    simpan = st.form_submit_button("💾 SIMPAN DATA")

if simpan:
    data_baru = pd.DataFrame([{
        "Tanggal": str(tanggal),
        "Jenis Ikan": jenis,
        "Jumlah": jumlah,
        "Berat (gram)": berat,
        "Panjang (cm)": panjang
    }])

    df = pd.concat([df, data_baru], ignore_index=True)
    df.to_csv(FILE, index=False)

    st.success("Data berhasil disimpan!")

# Dashboard
st.divider()
st.header("📊 Dashboard Pertumbuhan")

if not df.empty:
    df["Tanggal"] = pd.to_datetime(df["Tanggal"])
    df = df.sort_values("Tanggal")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total pencatatan", len(df))
    col2.metric("Berat terakhir", f"{df.iloc[-1]['Berat (gram)']} gram")
    col3.metric("Panjang terakhir", f"{df.iloc[-1]['Panjang (cm)']} cm")

    st.subheader("Grafik Pertumbuhan Berat")
    st.line_chart(
        df.set_index("Tanggal")["Berat (gram)"]
    )

    st.subheader("Grafik Pertumbuhan Panjang")
    st.line_chart(
        df.set_index("Tanggal")["Panjang (cm)"]
    )

    st.subheader("Riwayat Data")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇️ Download Data CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="data_pertumbuhan_ikan.csv",
        mime="text/csv"
    )

else:
    st.info("Belum ada data. Silakan masukkan data pengukuran ikan.")