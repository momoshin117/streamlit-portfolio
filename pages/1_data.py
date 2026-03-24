import streamlit as st
import pandas as pd
import numpy as np

# ===== ページ見出し =====
st.title("データ確認ページ")

# app.py で保存したDataFrameを取得
df = st.session_state.get("df")

# DataFrameが存在しない場合は警告を出して処理を止める
if df is None:
    st.info("先にトップ(app)でCSVをアップロードしてください。")
    st.stop()

# 以下は DataFrame が読み込めた場合のみ処理を進める
# 現在読み込まれているファイル名を表示
st.caption(f"ファイル: {st.session_state.get('filename', '')}")

# ===== 表示する列のフィルタ =====
st.subheader("フィルタ")

# 画面上で表示したい列を複数選べるようにする
cols = st.multiselect("表示する列（未選択=全列）", df.columns.tolist())

# 未選択なら全列を表示する
if cols:
    view_df = df[cols]
else:
    view_df = df

# ===== キーワード検索 =====
# どこかの列に指定した文字列を含む行だけを残す
keyword = st.text_input("検索（どこかの列に含まれる文字）")

# キーワードが入力されたときのみ処理を行う
if keyword:
    # 各行を残すかどうかの判定を入れる
    # 初期値として、すべての行を False（表示しない）にしておく
    # 行番号は view_df に合わせる
    mask = pd.Series(False, index=view_df.index)

    # 各列を文字列に変換して、keywordを含むかどうかを判定
    # 1つでも一致する列があれば、その行を残す（OR）
    # 数値型も文字列型で比較
    # 大文字・小文字の区別なし
    # 欠損値は False で扱う
    for c in view_df.columns:
        mask = mask | view_df[c].astype(str).str.contains(keyword, case=False, na=False)

    # 条件に合う行だけを抽出
    # DataFrame[]の中身が列名ではなく、True/False の Series（行の絞り込み）であることに注意
    view_df = view_df[mask]

# ===== 数値列の範囲フィルタ =====
st.subheader("数値フィルタ")

# 現在のview_dfの中から数値列だけを取得
# 数値列のカラム名のリストにする
num_column_names = view_df.select_dtypes(include=np.number).columns.tolist()

# 数値列のカラム名がある場合のみ以下の処理を行う
if num_column_names:
    # フィルタ対象となる数値列を選択
    target = st.selectbox("対象の数値列を選択", num_column_names)

    # 欠損値を除外して最小値・最大値を取得
    # 型が混ざっていることも想定して、float に揃えておく
    filter_num_df = view_df[target].dropna()
    low = float(filter_num_df.min())
    high = float(filter_num_df.max())

    # スライダーで表示範囲を指定
    # 初期値は全範囲にしておく
    vlow, vhigh = st.slider(f"{target}の範囲", low, high, (low, high))

    # 指定範囲に入る行だけを残す
    # between で範囲内かどうか True/False で絞り込んでいる
    view_df = view_df[view_df[target].between(vlow, vhigh)]

# ===== 表の表示 =====
# 全部の列が空になっている行は除外する
view_df = view_df.dropna(how="all")

# 絞り込み後のデータを表として表示する
st.dataframe(view_df, use_container_width=True)

# ===== CSVダウンロード =====

# 表示中のデータをCSV形式に変換（Excel文字化け対策で utf-8-sig）
# DataFrame の1列目の index は除外
csv_bytes = view_df.to_csv(index=False).encode("utf-8-sig")

# ダウンロードボタンを表示
st.download_button(
    "この表示結果をCSVでダウンロード",
    data=csv_bytes,
    file_name="filtered.csv",
    mime="text/csv"
)