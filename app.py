import streamlit as st
import pandas as pd

st.title("CSV Dashboard")

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.write("データの中身")
    st.dataframe(df)

    st.write("列を選んでグラフ表示")
    column = st.selectbox("列を選択", df.columns)

    st.line_chart(df[column])
