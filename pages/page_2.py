import pandas as pd
import streamlit as st
from app import load_data

# 毎回最新のデータを読み込む
data = load_data()

df = data["df"]
latest_month = data["latest_month"]
monthly_counts = data["monthly_counts"]
total_by_year = data["total_by_year"]

st.write("トレーニング記録を確認しましょう。")
st.markdown("### 📊 概要情報")
col1, col2, col3 = st.columns(3)

# データが0件、または統計情報が無い場合は早期表示
if df is None or df.empty or latest_month is None or total_by_year is None or total_by_year.empty:
    st.warning("データがありません（または統計を作成できるデータが不足しています）。")
else:
    # 最新月の受講回数 / 年数 / 総受講回数の表示
    with col1:
        st.metric(label=f"最新月（{latest_month['Year']}年/{latest_month['Month']}月）の受講回数", value=f"{int(latest_month['Count'])} 回")
    with col2:
        st.metric(label="年数", value=f"{len(total_by_year)} 年分")
    with col3:
        total_sum = total_by_year["Count"].sum()
        st.metric(label="総受講回数", value=f"{int(total_sum)} 回")

st.subheader("記録一覧（最新順）")
df = pd.read_csv("./data/b_monster_record.csv")

# データが0件の場合
if df is None or df.empty:
    st.warning("データがありません。")
else:
    try:
        st.dataframe(df.sort_values("Date", ascending=False))        
    except Exception:
        # 万が一 Date 列や変換で問題があれば、そのまま df を表示
        st.dataframe(df)
    
st.divider()
st.caption("© 2025 b-mon Analyzer | Streamlit + Matplotlib + Seaborn")