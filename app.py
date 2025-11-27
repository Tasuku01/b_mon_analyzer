import pandas as pd

# Time列の値を(朝・昼・夜)に変換する関数
def classify_time_period(t):
    try:
        hour = t.hour
        if 6 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 23:
            return "Evening"
        else:
            return "N.A"
    except AttributeError:
        return "N.A"

def load_data():
    # csvファイルを読み込む
    df = pd.read_csv("./data/b_monster_record.csv")
    
    # データが0件の時
    if df.empty:
        return {
            "df": df,
            "latest_month": None,
            "monthly_counts": pd.DataFrame(),
            "total_by_year": pd.DataFrame(),
            "heatmap_data": pd.DataFrame(),
            "performer_counts": pd.DataFrame(),
        }

    # 日付を変換
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # 欠損値除外
    df = df.dropna(subset=["Date"])

    # 時刻を変換
    # Time 列から「開始時刻」部分だけを抽出
    df["startTime"] = df["Time"].str.split("-").str[0]
    # 文字列を datetime に変換（ここは警告なしで安全）
    df["startTime"] = pd.to_datetime(df["startTime"], errors="coerce")
    # 時刻のみを取り出す (例: 07:00:00)
    df["Time"] = df["startTime"].dt.time

    # 年・月・を追加
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    # 曜日列を追加（.str[:3]で先頭から3文字だけ表示  例: Mon, Tue）
    df["Weekday"] = df["Date"].dt.day_name().str[:3]

    # 時間帯(TimePeriod)列を追加（Morning, Afternoon, Eveningを表示）
    df["TimePeriod"] = df["Time"].apply(classify_time_period)

    # 各年・各月の受講回数を集計
    monthly_counts = df.groupby(["Year", "Month"]).size().reset_index(name="Count")
    # monthly_counts が 1件以上あれば OK
    if len(monthly_counts) > 0:
        # 最新月の受講回数を集計
        latest_month = monthly_counts.iloc[-1]
    else:
        latest_month = None
    
    # 年間の総受講回数を集計
    total_by_year = monthly_counts.groupby("Year")["Count"].sum().reset_index()

    # パフォーマー別の受講回数を集計
    performer_counts = df["Performer"].value_counts().reset_index()

    # 可視化のための縦軸(Count)と横軸(Performer)を定義
    performer_counts.columns = ["Performer", "Count"]

    # 可視化のための曜日を定義
    weekday_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun",]

    # 可視化のための時間帯を定義(N.Aは不明を表す)
    time_order = ["Morning", "Afternoon", "Evening", "N.A"]

    # ヒートマップ（曜日 × 時間帯）の集計
    heatmap_data = pd.crosstab(df["TimePeriod"], df["Weekday"]).reindex(
        index=time_order, columns=weekday_order, fill_value=0
    )
    
    return {
        "df": df,
        "latest_month": latest_month,
        "monthly_counts": monthly_counts,
        "total_by_year": total_by_year,
        "heatmap_data": heatmap_data,
        "performer_counts": performer_counts,
    }
