import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ai_chat import ask_ai

st.set_page_config(page_title="AI Analytics Copilot", page_icon="📊", layout="wide")

st.title("🤖 AI Analytics Copilot")
st.write("Upload a CSV or Excel file and analyze it instantly.")

uploaded_file = st.sidebar.file_uploader(
    "Upload Dataset", type=["csv", "xlsx"]
)

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ Dataset Uploaded Successfully")

    # Preview
    st.subheader("📋 Dataset Preview")
    st.dataframe(df)

    # Metrics
    st.subheader("📊 Dataset Information")

    c1, c2, c3 = st.columns(3)

    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing Values", int(df.isnull().sum().sum()))

    # Data Types
    st.subheader("📝 Data Types")
    st.dataframe(df.dtypes.astype(str))

    # Statistics
    st.subheader("📈 Statistical Summary")
    st.dataframe(df.describe())

    # Missing Values
    st.subheader("❌ Missing Values")
    st.dataframe(df.isnull().sum())

    # Visualization
    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if len(numeric_columns) > 0:

        st.subheader("📊 Visualization")

        chart = st.selectbox(
            "Select Chart",
            ["Histogram", "Bar Chart", "Line Chart"]
        )

        column = st.selectbox(
            "Select Numeric Column",
            numeric_columns
        )

        if chart == "Histogram":
            fig = px.histogram(df, x=column)

        elif chart == "Bar Chart":
            fig = px.bar(df, x=df.index, y=column)

        else:
            fig = px.line(df, x=df.index, y=column)

        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👈 Upload a dataset to begin.")

    from utils.ai_chat import ask_ai

st.subheader("🤖 Ask AI About Your Dataset")

question = st.text_input("Ask any question")

if st.button("Generate AI Answer"):

    context = df.head(100).to_string()

    prompt = f"""
Dataset:

{context}

Question:

{question}

Give a clear answer.
"""

    answer = ask_ai(prompt)

    st.success(answer)

    st.divider()

st.header("🤖 AI Analytics Assistant")

question = st.text_input(
    "Ask a question about your dataset",
    placeholder="Example: Summarize this dataset"
)

if st.button("Ask AI"):

    with st.spinner("Analyzing dataset..."):

        dataset = df.head(100).to_string()

        prompt = f"""
You are a professional Data Analyst.

Dataset:

{dataset}

User Question:
{question}

Provide:
1. Clear answer
2. Key insights
3. Recommendations
"""

        answer = ask_ai(prompt)

        st.success(answer)