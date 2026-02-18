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

st.dataframe(view_df, use_container_width=True, height=520)

#数値
st.subhheader("数値フィルタ")

# ダウンロード
csv_bytes = view_df.to_csv(index=False).encode("utf-8-sig")
st.download_button("この表示結果をCSVでダウンロード", data=csv_bytes, file_name="filtered.csv", mime="text/csv")
