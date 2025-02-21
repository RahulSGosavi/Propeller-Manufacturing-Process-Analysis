
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# File Uploader
st.title(":bar_chart:Excel Data Visualization App")
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    print("Available columns:", df.columns.tolist())  # Debugging line


    # --- PLOT 1: PIE CHART (Matplotlib) ---
    status_counts = df["Status"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", colors=["green", "orange", "red"])
    ax1.set_title("Status Distribution")
    st.pyplot(fig1)

    # --- PLOT 2: LINE GRAPH (Plotly) ---
    fig2 = px.line(df, x=df.index, y=["Overall Efficiency", "Standard Overall Efficiency"],
                   title="Overall Efficiency vs Standard Efficiency")
    st.plotly_chart(fig2)

    # --- RESULT INSIGHTS ---
    st.subheader("🔍 Result Insights")
    
    # 1️⃣ Insights for Pie Chart (Status)
    most_common_status = status_counts.idxmax()
    st.write(f"✅ The most common status is **{most_common_status}** with **{status_counts.max()}** entries.")

    # 2️⃣ Insights for Efficiency
    avg_efficiency = df["Overall Efficiency"].mean()
    avg_standard = df["Standard Overall Efficiency"].mean()

    if avg_efficiency > avg_standard:
        efficiency_message = "Great! The overall efficiency is above the standard."
    elif avg_efficiency < avg_standard:
        efficiency_message = "⚠️ Warning: The overall efficiency is below the standard. Improvements are needed!"
    else:
        efficiency_message = "Efficiency is matching the standard perfectly."

    st.write(f"📊 The **average overall efficiency** is **{avg_efficiency:.2f}**, "
             f"while the **standard efficiency** is **{avg_standard:.2f}**.")
    st.write(efficiency_message)
