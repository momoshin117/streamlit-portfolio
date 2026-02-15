import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Dashboard", layout="wide")
st.title("CSV Dashboard")
st.caption("CSVをアップロードして、データ確認・可視化まで行います。")

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

if uploaded_file is None:
    st.info("まずはCSVをアップロードしてください。左メニューのページはアップロード後に使えます。")
    st.stop()

# 読み込み（文字化け対策は必要になったら追加）
df = pd.read_csv(uploaded_file)

# セッションに保存（別ページでも参照できる）
st.session_state["df"] = df
st.session_state["filename"] = uploaded_file.name

# サマリ表示
c1, c2, c3, c4 = st.columns(4)
c1.metric("行数", f"{df.shape[0]:,}")
c2.metric("列数", f"{df.shape[1]:,}")
c3.metric("欠損数", f"{int(df.isna().sum().sum()):,}")
c4.metric("重複行", f"{int(df.duplicated().sum()):,}")

st.subheader("プレビュー（先頭20行）")
st.dataframe(df.head(20), use_container_width=True)

with st.expander("列の型 / 欠損数"):
    info = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "missing": df.isna().sum(),
        "missing_rate": (df.isna().mean() * 100).round(2)
    })
    st.dataframe(info, use_container_width=True)

with st.expander("数値列の基本統計"):
    num = df.select_dtypes(include="number")
    if num.shape[1] == 0:
        st.warning("数値列がありません。")
    else:
        st.dataframe(num.describe().T, use_container_width=True)
