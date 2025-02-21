import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit App Configuration
st.set_page_config(layout="wide")

# Title
st.title("Propeller Performance Dashboard")

# Sidebar Section
st.sidebar.title("Time Conversion Helper")
units = st.sidebar.number_input("Enter number of units:", min_value=1.0, step=1.0, value=1.0)
minutes_per_unit = 120
converted_time = units * minutes_per_unit
st.sidebar.write(f"{units} units = {converted_time} minutes")

st.sidebar.subheader("Upload Excel or CSV File")
uploaded_file = st.sidebar.file_uploader("Choose an Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    
    # Clean column names
    df.columns = df.columns.str.strip().str.lower()
    
    expected_columns = ["propeller", "date", "time", "handler", "preforming (yet-to-start)", "preforming (in-progress)",
                        "moulding (yet-to-start)", "moulding (in-progress)", "cnc trimming", "trimming", "balancing", "polishing",
                        "quality", "performance", "packaging", "shipping"]
    missing_columns = [col for col in expected_columns if col not in df.columns]
    
    if not missing_columns:
        # Convert data for grouped comparison
        df_melted = df.melt(id_vars=["propeller", "date", "time", "handler"], 
                            var_name="stage", value_name="status")
        
        # Ensure decimal formatting for Time
        df_melted["time"] = df_melted["time"].astype(float).round(2)
        
        # Create Status Column if Missing
        if "status" not in df_melted.columns:
            df_melted["status"] = df_melted["stage"].apply(lambda x: "Completed" if "completed" in x.lower() else "In Progress")
        
        # Define color mapping
        color_map = {
            "Completed": "#1f77b4",  # Blue
            "In Progress": "#ff7f0e",  # Orange
            "Yet to Start": "#2ca02c"  # Green
        }
        
        # Sidebar Insights
        total_time = df_melted["time"].sum()
        avg_time_per_stage = df_melted.groupby("stage")["time"].mean().round(2)
        
        st.sidebar.subheader("Performance Insights")
        st.sidebar.write(f"Total Time Spent: {total_time} minutes")
        st.sidebar.write("Average Time per Stage:")
        st.sidebar.dataframe(avg_time_per_stage)
        
        # First Graph: Current Propeller vs. Batch Average
        fig1 = px.bar(df_melted, x="stage", y="time", color="status",
                      title="Current Propeller vs. Batch Average",
                      labels={"time": "Minutes", "stage": "Production Stage"},
                      barmode="group",
                      color_discrete_map=color_map)
        
        # Second Graph: Stacked Bar Chart for Time Distribution
        fig2 = px.bar(df_melted, x="stage", y="time", color="status",
                      title="Time Distribution Across Stages",
                      labels={"time": "Minutes", "stage": "Production Stage"},
                      barmode="stack",
                      color_discrete_map=color_map)
        
        # Improve layout
        fig1.update_layout(bargap=0.2, bargroupgap=0.1)
        fig2.update_layout(bargap=0.2, bargroupgap=0.1)
        
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.error(f"The uploaded file is missing required columns: {missing_columns}")
else:
    st.warning("Please upload a file to generate the graphs.")
