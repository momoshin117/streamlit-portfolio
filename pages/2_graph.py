import streamlit as st
import pandas as pd
import numpy as np

# ===== ページ見出し =====
st.title("グラフページ")

# app.py で保存したDataFrameを取得
df = st.session_state.get("df")

# DataFrameが存在しない場合はメッセージを出して処理を止める
if df is None:
    st.info("先にトップ(app)でCSVをアップロードしてください。")
    st.stop()

# 数値列と数値以外の列の名前をリストで取得
num_column_names = df.select_dtypes(include=np.number).columns.tolist()
non_num_column_names = df.select_dtypes(exclude=np.number).columns.tolist()

# 数値以外の列はグラフを作成できないため除外
if not num_column_names:
    st.warning("数値列がないためグラフを作れません。")
    st.stop()

# ===== グラフ設定 =====

# # 数値のフィルタ
# target = st.selectbox("フィルタする列", num_column_names)
# filter_num_df = df[target].dropna()
# low = float(filter_num_df.min())
# high = float(filter_num_df.max())
#
# vlow, vhigh = st.slider(f"{target}の範囲", low, high, (low, high))
# df = df[df[target].between(vlow, vhigh)]

# グラフの種類を選ぶ
chart_type = st.selectbox("グラフ種類", ["折れ線", "棒", "ヒストグラム", "散布図"])

# ===== 折れ線・棒グラフ・ヒストグラム =====
if chart_type in ["折れ線", "棒", "ヒストグラム"]:

    # グラフにする数値列を選ぶ
    y = st.selectbox("数値列（Y）", num_column_names)
    st.write("プレビュー")

    # 折れ線の場合
    if chart_type == "折れ線":
        st.line_chart(df[y])

    # 棒グラフの場合
    elif chart_type == "棒":
        st.bar_chart(df[y])

    # ヒストグラムの場合
    else:
        # ヒストグラムの区間数を選ぶ（範囲：5〜100、初期値：20）
        bins = st.slider("bins", 5, 100, 20)

        # 値を区間に分けて件数を集計する
        # pd.cut でそれぞれのデータがどの区間に入るか変換
        # hist_data は、区間ごとの件数を持った Series
        hist_data = pd.cut(df[y].dropna(), bins=bins).value_counts().sort_index()

        # 集計結果を棒グラフとして表示する
        st.bar_chart(hist_data)

# ===== 散布図 =====
else:
    x = st.selectbox("X（数値）", num_column_names, index=0)
    y = st.selectbox("Y（数値）", num_column_names, index=min(1, len(num_column_names) - 1))
    st.scatter_chart(df[[x, y]].dropna())