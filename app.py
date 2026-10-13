import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Student Result Analyzer", page_icon="📊", layout="centered"
)

st.title("🎓 Student Performance & Result Analyzer")
st.write(
    "Upload any student dataset (CSV or Excel) to instantly generate performance"
    " metrics, summaries, and distribution charts."
)

# File uploader widget
uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file", type=["csv", "xlsx"]
)

if uploaded_file is not None:
  try:
    # Read file based on extension
    if uploaded_file.name.endswith(".csv"):
      df = pd.read_csv(uploaded_file)
    else:
      df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

    # Display raw data preview
    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head())

    # Basic Analysis / Summary Metrics
    st.subheader("📈 Quick Performance Analytics")
    if "SGPA" in df.columns and "CGPA" in df.columns:
      col1, col2, col3 = st.columns(3)
      with col1:
        st.metric("Total Students", len(df))
      with col2:
        st.metric("Average SGPA", round(df["SGPA"].mean(), 2))
      with col3:
        st.metric("Average CGPA", round(df["CGPA"].mean(), 2))

      # Pass / Fail distribution if RESULT column exists
      if "RESULT" in df.columns:
        st.subheader("🏆 Status Distribution")
        status_counts = df["RESULT"].value_counts()
        st.bar_chart(status_counts)
    else:
      st.info(
          "Columns 'SGPA', 'CGPA', or 'RESULT' not found. Displaying general"
          " row count."
      )
      st.metric("Total Rows", len(df))

    # Download processed button
    st.download_button(
        label="Download Processed Report",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="processed_result_report.csv",
        mime="text/csv",
    )

  except Exception as e:
    st.error(f"Error processing file: {e}")