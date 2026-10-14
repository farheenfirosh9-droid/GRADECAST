import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Student Result Analyzer",
    page_icon="📊",
    layout="centered"
)

st.title("🎓 Student Performance & Result Analyzer")

st.write(
    "Upload any student dataset (CSV or Excel) to instantly generate performance "
    "metrics, summaries, and distribution charts."
)

# File uploader widget
uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
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

            # Top Performers Leaderboard
            st.subheader("🏆 Top Performers Leaderboard")

            # Select ranking criteria
            rank_by = st.selectbox(
                "Rank students by",
                ["CGPA", "SGPA"]
            )

            # Select number of top students
            top_n = st.radio(
                "Show Top Performers",
                [3, 5],
                horizontal=True
            )

            # Find student name column
            name_columns = [
                "NAME",
                "Name",
                "name",
                "STUDENT NAME",
                "Student Name",
                "STUDENT_NAME"
            ]

            name_col = next(
                (col for col in name_columns if col in df.columns),
                None
            )

            # Convert selected scores to numeric values
            ranking_df = df.copy()

            ranking_df[rank_by] = pd.to_numeric(
                ranking_df[rank_by],
                errors="coerce"
            )

            # Remove rows with invalid scores
            ranking_df = ranking_df.dropna(subset=[rank_by])

            # Sort and select top performers
            ranking_df = ranking_df.sort_values(
                by=rank_by,
                ascending=False
            ).head(top_n)

            if not ranking_df.empty:
                for rank, (_, student) in enumerate(
                    ranking_df.iterrows(),
                    start=1
                ):
                    trophies = {
                        1: "🥇",
                        2: "🥈",
                        3: "🥉"
                    }

                    medal = trophies.get(rank, "🏅")

                    if name_col:
                        student_name = student[name_col]
                    else:
                        student_name = f"Student {rank}"

                    st.write(
                        f"{medal} **Rank {rank}: {student_name}** "
                        f"— {rank_by}: {student[rank_by]:.2f}"
                    )
            else:
                st.info("No valid scores available for ranking.")

            # Pass / Fail distribution if RESULT column exists
            if "RESULT" in df.columns:
                st.subheader("📊 Status Distribution")
                status_counts = df["RESULT"].value_counts()
                st.bar_chart(status_counts)

        else:
            st.info(
                "Columns 'SGPA' and 'CGPA' not found. "
                "Displaying general row count."
            )

            st.metric("Total Rows", len(df))

        # Download processed report
        st.download_button(
            label="Download Processed Report",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="processed_result_report.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error processing file: {e}")