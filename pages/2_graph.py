import streamlit as st
import pandas as pd
import numpy as np

st.title("グラフページ")

df = st.session_state.get("df")
if df is None:
    st.info("先にトップ(app)でCSVをアップロードしてください。")
    st.stop()

num_cols = df.select_dtypes(include=np.number).columns.tolist()
cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()

if not num_cols:
    st.warning("数値列がないためグラフを作れません。")
    st.stop()

# #数値のフィルタ
# target = st.selectbox("フィルタする列", num_cols)
# filter_num_df = df[target].dropna()
# low = float(filter_num_df.min())
# high = float(filter_num_df.max())

# vlow, vhigh = st.slider(f"{target}の範囲", low, high, (low,high))
# df = df[df[target].between(vlow, vhigh)]

chart_type = st.selectbox("グラフ種類", ["折れ線", "棒", "ヒストグラム", "散布図"])

if chart_type in ["折れ線", "棒", "ヒストグラム"]:
    y = st.selectbox("数値列（Y）", num_cols)
    st.write("プレビュー")
    if chart_type == "折れ線":
        st.line_chart(df[y])
    elif chart_type == "棒":
        st.bar_chart(df[y])
    else:
        bins = st.slider("bins", 5, 100, 20)
        st.histogram = st.bar_chart(pd.cut(df[y].dropna(), bins=bins).value_counts().sort_index())
else:
    x = st.selectbox("X（数値）", num_cols, index=0)
    y = st.selectbox("Y（数値）", num_cols, index=min(1, len(num_cols)-1))
    st.scatter_chart(df[[x, y]].dropna())

