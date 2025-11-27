import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from app import load_data

df = pd.read_csv("./data/b_monster_record.csv")

# データを毎回読み込む
data = load_data()
monthly_counts = data["monthly_counts"]
total_by_year = data["total_by_year"]
heatmap_data = data["heatmap_data"]
performer_counts = data["performer_counts"]

st.markdown("### 📈 カテゴリ別データ集計結果")

tab1, tab2, tab3, tab4 = st.tabs([
    "📅 年別・月別受講回数の推移", 
    "📆 年別の総受講回数", 
    "🕒 曜日 × 時間帯の受講傾向",
    "🧑‍🏫 パフォーマー別受講回数", 
])

# データが無い場合は警告して終了
if (
    df is None or df.empty or
    monthly_counts is None or monthly_counts.empty or
    total_by_year is None or total_by_year.empty or
    heatmap_data is None or heatmap_data.empty or
    performer_counts is None or performer_counts.empty
):
    st.warning("データがありません")
    st.stop()

# --------------------------------------------------
# 年別・月別受講回数（折れ線グラフ）: tab1
# --------------------------------------------------
    
with tab1:
    # 折れ線グラフ作成
    st.subheader("年別・月別受講回数の推移")
    
    # 折れ線グラフの表示サイズを定義
    fig, ax = plt.subplots(figsize=(8, 4))
    
    for year in sorted(monthly_counts["Year"].unique()):
        year_data = monthly_counts[monthly_counts["Year"] == year]
        ax.plot(year_data["Month"], year_data["Count"], marker="o", label=str(year))
        
    # 折れ線グラフのレイアウト設定(x軸:Month, y軸:Count 凡例有り)
    ax.set_xlabel("Month")
    ax.set_ylabel("Count")
    ax.set_xticks([i for i in range(1, 13)])
    ax.set_yticks([i for i in range(0, 20)])
    ax.legend(title="Year")
    ax.grid(True)
        
    # グラフのレイアウトを調整    
    plt.tight_layout()
                
    # 折れ線グラフを画面に表示
    st.pyplot(fig,use_container_width=False)

# --------------------------------------------------
# 年別の総受講回数（棒グラフ）: tab2
# --------------------------------------------------
with tab2:
    
    total_by_year = monthly_counts.groupby("Year")["Count"].sum().reset_index()
    
    # x軸(Year)を文字列に型変換
    total_by_year["Year"] = total_by_year["Year"].astype(str)

    st.subheader("年別の総受講回数")
    
    # 棒グラフの表示サイズを定義
    fig2, ax2 = plt.subplots(figsize=(4, 4))
    
    # 棒グラフの作成(x軸:Year, y軸:Count)
    ax2.bar(total_by_year["Year"], total_by_year["Count"], edgecolor = "black")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Count")
    
    # 年別の総受講回数を棒グラフ上に数値で表示
    for i, v in enumerate(total_by_year["Count"]):
        ax2.text(total_by_year["Year"].iloc[i], v + 0.5, str(v), ha="center")
    
    # グラフのレイアウトを調整    
    plt.tight_layout()
    
    # 棒グラフを画面に表示
    st.pyplot(fig2, use_container_width=False)

# --------------------------------------------------
# 曜日 × 時間帯（ヒートマップ） : tab3
# --------------------------------------------------
with tab3:
    st.subheader("曜日 × 時間帯の受講傾向")
    
    # ヒートマップの表示サイズを定義
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    
    # ヒートマップの描画(x軸:Day of Week, y軸:Time of Period)
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="OrRd", cbar=True, linewidths=0.5, ax=ax3)
    ax3.set_xlabel("Day of Week")
    ax3.set_ylabel("Time of Period")
    ax3.set_yticklabels(ax3.get_yticklabels(), rotation=0)
    
    # グラフのレイアウトを調整 
    plt.tight_layout()
    
    # ヒートマップを画面に表示
    st.pyplot(fig3, use_container_width=False)
    
# --------------------------------------------------
# パフォーマー別受講回数（横棒グラフ）: tab4
# --------------------------------------------------
with tab4:
    st.subheader("パフォーマー別の受講回数")
    st.write("トップ3を黄色で表示")
    # 受講回数の多い順に並べる
    performer_counts = performer_counts.sort_values("Count", ascending=True)
        
    # トップ3をゴールドで強調
    colors = ["gold" if i >= len(performer_counts) - 3 else "lightgray" for i in range(len(performer_counts))]
        
    # 横棒グラフの作成
    fig4, ax4 = plt.subplots(figsize=(7,8))
    ax4.barh(performer_counts["Performer"], performer_counts["Count"], color=colors, edgecolor="black")
    ax4.set_xlabel("Count")
    ax4.set_ylabel("Performer")
        
    # 件数ラベルを追加
    for i, v in enumerate(performer_counts["Count"]):
        ax4.text(v + 0.3, i, str(v), va="center")
        
    plt.tight_layout()
    st.pyplot(fig4, use_container_width=False)

st.divider()   
st.caption("© 2025 b-mon Analyzer | Streamlit + Matplotlib + Seaborn")