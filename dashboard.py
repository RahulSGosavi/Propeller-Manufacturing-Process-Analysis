import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit app title
st.title("📊 Propeller Manufacturing Process Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    try:
        # Load dataset
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        
        # Define required columns
        required_columns = [
            "Propeller ID", "Date", "Time", "Handler",
            "Preforming (Yet-to-Start)", "Preforming (In-Progress)", 
            "Moulding (Yet-to-Start)", "Moulding (In-Progress)", 
            "CNC Trimming", "Trimming", "Balancing", "Polishing",
            "Quality", "Performance", "Packaging", "Shipping"
        ]
        
        # Validate columns
        if all(col in df.columns for col in required_columns):
            st.success("✅ File successfully uploaded and validated!")
            
            # Select Propeller ID
            propeller_options = df["Propeller ID"].unique()
            selected_propeller = st.selectbox("Select a Propeller ID:", propeller_options)

            # Filter data for selected propeller
            propeller_data = df[df["Propeller ID"] == selected_propeller]

            if not propeller_data.empty:
                # Melt DataFrame for better visualization
                melted_df = propeller_data.melt(id_vars=["Propeller ID"], 
                                                value_vars=required_columns[4:], 
                                                var_name="Stage", 
                                                value_name="Value")

                # Plot comparison
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.barplot(data=melted_df, x="Stage", y="Value", palette="coolwarm", ax=ax)
                
                ax.set_title(f"Comparison for {selected_propeller}")
                ax.set_ylabel("Value")
                ax.set_xlabel("")
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
                
                # Display the plot
                st.pyplot(fig)

            else:
                st.warning("⚠ No data available for the selected propeller.")

        else:
            missing_cols = [col for col in required_columns if col not in df.columns]
            st.error(f"⚠ Missing columns: {missing_cols}. Please upload a file with all required columns.")

    except Exception as e:
        st.error(f"Error loading file: {e}")
