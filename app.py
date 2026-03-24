import streamlit as st
import pandas as pd

# ===== ページ設定・見出し =====
st.set_page_config(page_title="CSV Dashboard", layout="wide")
st.title("ホーム")
st.caption("CSVをアップロードして、データ確認・可視化まで行います。")

# ===== CSVファイルのアップロード =====
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

# ===== ファイル未選択時の処理 =====
# ファイルがアップロードされるまで以降の処理を止める
if uploaded_file is None:
    st.info("まずはCSVをアップロードしてください。左メニューのページはアップロード後に使えます。")
    st.stop()

# ===== 読み込み =====
# 文字化け対策は必要になったら追加
df = pd.read_csv(uploaded_file)

# ===== セッションに保存 =====
# 別ページでも参照できる
st.session_state["df"] = df
st.session_state["filename"] = uploaded_file.name

# ===== データの概要を表示 =====
# データが大きいことも想定して、3桁区切りとする
c1, c2, c3, c4 = st.columns(4)
c1.metric("行数", f"{df.shape[0]:,}")
c2.metric("列数", f"{df.shape[1]:,}")

# df.isna() で各セルが欠損しているか判定。
# .sum()で列ごとに集計後、さらに.sum()で全セル分を集計
c3.metric("欠損数", f"{int(df.isna().sum().sum()):,}")

# df.duplicated() で各行が前に出てきた行と重複しているか判定(1次元)。
c4.metric("重複行", f"{int(df.duplicated().sum()):,}")

st.subheader("プレビュー（先頭20行）")
st.dataframe(df.head(20), use_container_width=True)

# ===== 列ごとの情報を表示 =====
# 各列のデータ型、欠損数、欠損率を確認できる表を表示する
with st.expander("列の型 / 欠損数"):
    # 新たな DataFrame: info
    # df から列の型・欠損数・欠損率を抜き出した DataFrame
    info = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "missing": df.isna().sum(),
        # .mean()で True=1, False=0 として平均を取る
        "missing_rate": (df.isna().mean() * 100).round(2)
    })
    st.dataframe(info, use_container_width=True)

# ===== 統計情報 =====
# 数値型の列だけを抽出し、統計情報を表示する
with st.expander("統計情報"):
    # 新たな DataFrame: num
    # df から数値列だけを抜き出した DataFrame
    num = df.select_dtypes(include="number")

    # shape(行数, 列数)で列数が存在するかチェック
    if num.shape[1] == 0:
        st.warning("数値列がありません。")
    else:
        # describe() で統計情報を出す
        # 件数, 平均, 標準偏差, 最小値, 第1四分位数, 中央値, 第3四分位数, 最大値
        # 列ごとの統計情報を見やすくするために転置する
        st.dataframe(num.describe().T, use_container_width=True)