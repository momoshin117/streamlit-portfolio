import streamlit as st
import pandas as pd
import numpy as np

st.title("データ確認ページ")

df = st.session_state.get("df")
if df is None:
    st.info("先にトップ(app)でCSVをアップロードしてください。")
    st.stop()

st.caption(f"ファイル: {st.session_state.get('filename','')}")

# フィルタ
st.subheader("フィルタ")
cols = st.multiselect("表示する列（未選択=全列）", df.columns.tolist())
view_df = df[cols] if cols else df

# 簡易検索（文字列を含む行）
keyword = st.text_input("検索（どこかの列に含まれる文字）")
if keyword:
    mask = pd.Series(False, index=view_df.index)
    for c in view_df.columns:
        mask = mask | view_df[c].astype(str).str.contains(keyword, case=False, na=False)
    view_df = view_df[mask]

#数値のフィルター
st.subheader("数値フィルタ")
num_cols = view_df.select_dtypes(include=np.number).columns.tolist()

if num_cols:
    target = st.selectbox("対象の数値列を選択", num_cols)

    filter_num_df = view_df[target].dropna()    #欠損列の削除
    low = float(filter_num_df.min())
    high = float(filter_num_df.max())

    vlow, vhigh = st.slider(f"{target}の範囲", low, high, (low, high))
    view_df = view_df[view_df[target].between(vlow, vhigh)]

#表の描画
view_df = view_df.dropna(how="all")     #不要な列を削除
st.dataframe(view_df, use_container_width=True)

# ダウンロード
csv_bytes = view_df.to_csv(index=False).encode("utf-8-sig")
st.download_button("この表示結果をCSVでダウンロード", data=csv_bytes, file_name="filtered.csv", mime="text/csv")
