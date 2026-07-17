import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from backend.database import create_table, save_prediction, get_history
# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("saved_model/cyber_model.pkl")
label_encoder = joblib.load("saved_model/label_encoder.pkl")

# Create database table
create_table()

# -----------------------------
# Streamlit Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Cyber Threat Intelligence",
    page_icon="🛡",
    layout="wide"
)

st.title("🛡 Cyber Threat Intelligence & Attack Detection System")
st.markdown("---")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Prediction",
        "History",
        "Analytics",
        "Dataset",
        "About"
    ]
)

# =====================================================
# Dashboard
# =====================================================

if page == "Dashboard":

    df = pd.read_csv("dataset/raw/cyberthreat.csv")

    st.header("📊 Dashboard")

    total_records = len(df)
    total_features = len(df.columns)
    attack_types = df["Label"].nunique()
    safe_records = len(df[df["Label"] == "BENIGN"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📄 Total Records", total_records)
    col2.metric("📑 Total Features", total_features)
    col3.metric("🚨 Attack Types", attack_types)
    col4.metric("✅ Safe Traffic", safe_records)

    st.write("---")

    st.subheader("Recent Dataset")

    st.dataframe(df.head(), use_container_width=True)

    st.write("---")

    st.subheader("Attack Distribution")

    fig, ax = plt.subplots(figsize=(8,4))

    df["Label"].value_counts().plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Attack Type")
    ax.set_ylabel("Count")

    st.pyplot(fig)
    # =====================================================
# Prediction Page
# =====================================================

elif page == "Prediction":

    st.header("🚀 Attack Prediction")

    col1, col2 = st.columns(2)

    with col1:
        flow_id = st.number_input("Flow ID", value=1)
        source_ip = st.number_input("Source IP (Encoded)", value=0)
        destination_ip = st.number_input("Destination IP (Encoded)", value=0)
        source_port = st.number_input("Source Port", value=80)
        destination_port = st.number_input("Destination Port", value=8080)
        protocol = st.number_input("Protocol (Encoded)", value=0)

    with col2:
        flow_duration = st.number_input("Flow Duration (ms)", value=1000)
        total_fwd = st.number_input("Total Fwd Packets", value=10)
        total_bwd = st.number_input("Total Bwd Packets", value=10)
        flow_bytes = st.number_input("Flow Bytes/s", value=10000)
        flow_packets = st.number_input("Flow Packets/s", value=10.0)

    if st.button("🚀 Predict Attack"):

        sample = np.array([[
            flow_id,
            source_ip,
            destination_ip,
            source_port,
            destination_port,
            protocol,
            flow_duration,
            total_fwd,
            total_bwd,
            flow_bytes,
            flow_packets
        ]])

        prediction = model.predict(sample)
        attack = label_encoder.inverse_transform(prediction)

        # Save prediction to SQLite database
        save_prediction(attack[0])
        st.subheader("Prediction Result")

        if attack[0] == "BENIGN":
            st.success("✅ Network Traffic is Safe")
        else:
            st.error(f"🚨 Attack Detected : {attack[0]}")

# =====================================================
# Prediction History
# =====================================================

elif page == "History":

    st.header("📜 Prediction History")

    history = get_history()

    if len(history) == 0:

        st.info("No predictions available.")

    else:

        history_df = pd.DataFrame(
            history,
            columns=[
                "ID",
                "Flow ID",
                "Source IP",
                "Destination IP",
                "Protocol",
                "Prediction",
                "Date & Time"
            ]
        )

        st.dataframe(history_df, use_container_width=True)

        st.write("---")

        st.subheader("Recent Predictions")

        st.dataframe(
            history_df.head(10),
            use_container_width=True
        )
        # =====================================================
# Analytics Page
# =====================================================

elif page == "Analytics":

    st.header("📈 Cyber Threat Analytics")

    df = pd.read_csv("dataset/raw/cyberthreat.csv")

    col1, col2 = st.columns(2)

    # -----------------------------
    # Attack Distribution (Bar Chart)
    # -----------------------------
    with col1:

        st.subheader("📊 Attack Distribution")

        fig, ax = plt.subplots(figsize=(6, 4))

        df["Label"].value_counts().plot(
            kind="bar",
            color="steelblue",
            ax=ax
        )

        ax.set_xlabel("Attack Type")
        ax.set_ylabel("Count")

        st.pyplot(fig)

    # -----------------------------
    # Pie Chart
    # -----------------------------
    with col2:

        st.subheader("🥧 Attack Percentage")

        fig2, ax2 = plt.subplots(figsize=(5, 5))

        df["Label"].value_counts().plot(
            kind="pie",
            autopct="%1.1f%%",
            ax=ax2
        )

        ax2.set_ylabel("")

        st.pyplot(fig2)

    st.write("---")

    # -----------------------------
    # Flow Bytes Graph
    # -----------------------------
    st.subheader("📈 Flow Bytes/s")

    flow_bytes = (
        df["Flow Bytes/s"]
        .astype(str)
        .str.replace(",", "")
        .astype(float)
    )

    st.line_chart(flow_bytes)

    st.write("---")

    # -----------------------------
    # Flow Packets Graph
    # -----------------------------
    st.subheader("📉 Flow Packets/s")

    st.bar_chart(df["Flow Packets/s"])

# =====================================================
# Dataset Page
# =====================================================

elif page == "Dataset":

    st.header("📂 Dataset Overview")

    df = pd.read_csv("dataset/raw/cyberthreat.csv")

    # -----------------------------
    # Statistics
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("📄 Total Records", len(df))
    col2.metric("📑 Total Features", len(df.columns))
    col3.metric("🚨 Attack Types", df["Label"].nunique())

    st.write("---")

    # -----------------------------
    # Dataset Preview
    # -----------------------------
    st.subheader("Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.write("---")

    # -----------------------------
    # Dataset Information
    # -----------------------------
    st.subheader("Dataset Information")

    info_df = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str)
    })

    st.dataframe(
        info_df,
        use_container_width=True
    )

    st.write("---")

    # -----------------------------
    # Missing Values
    # -----------------------------
    st.subheader("Missing Values")

    missing = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(
        missing,
        use_container_width=True
    )
    # =====================================================
# About Page
# =====================================================

elif page == "About":

    st.header("ℹ️ About Project")

    st.markdown("""
    ## 🛡 Cyber Threat Intelligence & Attack Detection System

    This project is developed to detect cyber attacks using Machine Learning.

    ### 🎯 Project Objective

    Predict whether incoming network traffic is:

    - ✅ BENIGN
    - 🚨 DDoS
    - 🚨 Brute Force
    - 🚨 FTP-Patator
    - 🚨 SSH-Patator
    - 🚨 PortScan
    - 🚨 Bot Attack
    - 🚨 Web Attack

    ### 🤖 Machine Learning

    - Random Forest Classifier

    ### 🛠 Technologies Used

    - Python
    - Streamlit
    - Pandas
    - NumPy
    - Scikit-learn
    - Matplotlib
    - SQLite
    - Joblib

    ### 📂 Project Modules

    ✅ Dashboard

    ✅ Prediction

    ✅ Prediction History

    ✅ Analytics

    ✅ Dataset

    ### 🚀 Future Enhancements

    - User Login
    - Real-time Packet Capture
    - Live Network Monitoring
    - PDF Report Generation
    - Email Alerts
    - Cloud Deployment
    - Threat Severity Detection

    ---
    **Developed for Cyber Threat Intelligence using Machine Learning**
    """)