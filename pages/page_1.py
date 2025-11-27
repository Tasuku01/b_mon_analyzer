import streamlit as st
import pandas as pd
import csv
import os
import datetime
import time

csv_file = "./data/b_monster_record.csv"
df = pd.read_csv(csv_file)


#######################
#　変数定義
#######################
studios = ["GINZA", "OMOTESANDO", "EBISU", "SHINJUKU", "IKEBUKURO", "UMEDA", "NAGOYA"]
times = ["07:00-07:45", "08:15-09:10", "09:50-10:45", "11:25-12:20", "12:50-13:45",
         "14:15-15:10", "15:40-16:35", "17:05-18:00", "18:30-19:25", "19:55-20:50", "21:20-22:15"]
performers = ["ACE", "JELLENA", "KAORI", "KATE", "Lilly", "RAMI", "YUUHI", "SATSUKI", "TOA", "other"]
performers_shinjuku = ["DIO", "KALN", "Kenny", "other"]
programs = ["MIX1", "MIX2", "MIX3", "MIX4", "MIX5", "MIX0","k-pop", "k-pop2", "k-pop4","EDM1", "EDM2", "EDM0", "HARD", "HOUSE1", "Ad live", "Lite", "other"]
levels = ["★" * i for i in range(6)]
intensities = levels

# session_state 初期化
for key in ["temp_msg_text", "temp_msg_type", "confirm_delete"]:
    st.session_state.setdefault(key, None)

# csvファイルのIdのカラムに自動採番する関数
def get_next_id(csv_file):
    if not os.path.exists(csv_file):
        return 1
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        if len(reader) <= 1:
            return 1
        return int(reader[-1][0]) + 1

########################################
# メッセージ（保存・削除後の 2 秒表示）
########################################
if st.session_state.get("temp_msg_text"):
    msg_box = st.empty()
    if st.session_state.temp_msg_type == "success":
        msg_box.success(st.session_state.temp_msg_text)
    else:
        msg_box.error(st.session_state.temp_msg_text)
    
    # 2秒間だけ表示
    time.sleep(2)

    # メッセージを消去
    st.session_state.temp_msg_text = None
    st.session_state.temp_msg_type = None
    st.rerun()

#######################
#　登録フォーム
#######################

st.subheader("登録画面")
with st.expander("登録フォーム", expanded=False):
    st.write("下記の事項を全て入力してください。")

    # 動的に動く部分
    input_date = st.date_input("受講日", value=datetime.date.today())
    studio = st.selectbox("スタジオ", studios, index=2)
    time_slot = st.selectbox("受講時間", times)

    if studio == "SHINJUKU":
        performer = st.selectbox("パフォーマー（選択肢に無い場合は other を選択）", performers_shinjuku)
    else:
        performer = st.selectbox("パフォーマー（選択肢に無い場合は other を選択）", performers)

    # other 選択時に表示
    custom_performer = ""
    if performer == "other":
        custom_performer = st.text_input("パフォーマーを入力してください")

    program = st.selectbox("プログラム（選択肢に無い場合は other を選択）", programs)

    # other 選択時に表示
    custom_program = ""
    if program == "other":
        custom_program = st.text_input("プログラムを入力してください")

    level = st.selectbox("難易度（不明の場合は未入力でも可）", levels)
    intensity = st.selectbox("強度（不明の場合は未入力でも可）", intensities)

    # -------------------------
    # 登録フォーム
    # -------------------------
    with st.form("submit_form"):
        submit_button = st.form_submit_button("📝登録")
        
        
    # 登録処理後に記録を表示
    if submit_button:
        final_performer = custom_performer if performer == "other" else performer
        final_program = custom_program if program == "other" else program
        
        if performer == "other" and not custom_performer:
            st.error("パフォーマーを入力してください。")
            st.stop()
        
        if program == "other" and not custom_program:
            st.error("プログラムを入力してください。")
            st.stop()

        id = get_next_id(csv_file)
        date = input_date.strftime("%Y/%m/%d")

        record = [id, date, studio, time_slot, final_performer, final_program, level, intensity]

        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(record)
        
        st.session_state.show_msg = True
        st.session_state.msg_text = "登録しました！"
        st.success("登録しました！")
        st.session_state.msg_type = "success"
        time.sleep(2)
        st.rerun()

        
st.divider()

#######################
#　編集・削除フォーム
#######################

st.subheader("編集・削除画面")
with st.expander("編集・削除フォーム", expanded=False):


    # まずIDを選択
    Date_list = sorted(df["Date"].unique(), reverse=True)
    selected_date = st.selectbox("編集する 日付 を選んでください", Date_list)

    # 選択されたIDのDate一覧だけ抽出
    Id_list = sorted(df[df["Date"] == selected_date]["Id"].unique(), reverse=True)
    selected_Id = st.selectbox("編集する Id を選んでください", Id_list)

    # --- ID + Date の複合キーでレコード取得 ---
    target_df = df[(df["Date"] == selected_date) & (df["Id"] == selected_Id)]

    if target_df.empty:
        st.error("該当する記録が見つかりません。")
        st.stop()

    # 1件だけ取り出す
    target = target_df.iloc[0]

    st.write(f"### 編集中の記録：{selected_date} , Id：{selected_Id}")

    # --- 編集フォーム ---
    # 編集前の元データを初期値に設定する
    studio_index = studios.index(target["Studio"])
    time_index = times.index(target["Time"])

    new_date = st.date_input("受講日", pd.to_datetime(target["Date"]), key=f"edit_date_{selected_Id}_{selected_date}")
    new_studio = st.selectbox("スタジオ", studios, index=studio_index, key=f"edit_studio_{selected_Id}_{selected_date}")
    new_time = st.selectbox("受講時間", times, index=time_index, key=f"edit_time_{selected_Id}_{selected_date}")
    new_performer = st.text_input("パフォーマー", target["Performer"], key=f"edit_performer_{selected_Id}_{selected_date}")
    new_program = st.text_input("プログラム", target["Program"], key=f"edit_program_{selected_Id}_{selected_date}")
    new_level = st.selectbox("難易度（不明の場合は未入力でも可）", levels, key=f"edit_level_{selected_Id}_{selected_date}")
    new_intensity = st.selectbox("強度（不明の場合は未入力でも可）", intensities, key=f"edit_intensity_{selected_Id}_{selected_date}")

    with st.form("save_form"):
        c1, c2 = st.columns([1, 1])
        save_button = c1.form_submit_button("💾保存")
        delete_button = c2.form_submit_button("❌削除")

    # -------------------------
    # 保存処理
    # -------------------------
    if save_button:
        # 該当行だけ更新
        df.loc[(df["Id"] == selected_Id) & (df["Date"] == selected_date), "Date"] = new_date.strftime("%Y/%m/%d")
        df.loc[(df["Id"] == selected_Id) & (df["Date"] == selected_date), "Studio"] = new_studio
        df.loc[(df["Id"] == selected_Id) & (df["Date"] == selected_date), "Time"] = new_time
        df.loc[(df["Id"] == selected_Id) & (df["Date"] == selected_date), "Performer"] = new_performer
        df.loc[(df["Id"] == selected_Id) & (df["Date"] == selected_date), "Program"] = new_program
        df.loc[(df["Id"] == selected_Id) & (df["Date"] == selected_date), "Level"] = new_level
        df.loc[(df["Id"] == selected_Id) & (df["Date"] == selected_date), "Intensity"] = new_intensity
        
        # CSV 上書き保存
        df.to_csv("./data/b_monster_record.csv", index=False, encoding="utf-8")
        
        st.session_state.show_msg = True
        st.session_state.msg_text = "保存しました！"
        st.success("保存しました！")
        st.session_state.msg_type = "success"
        time.sleep(2)
        st.rerun()

    # -------------------------
    # 削除処理
    # -------------------------
    if delete_button:
        # 「確認中」フラグ ON
        st.session_state.confirm_delete = True
        st.rerun()

    # 削除確認表示 
    if st.session_state.get("confirm_delete", False):
        st.error("本当に削除しますか？ この操作は取り消せません。")
            
        cc1, cc2 = st.columns(2)
        with c1:
            if cc1.button("はい、削除する", type="primary"):
                
                # 削除
                df = df.drop(target_df.index)
                df.to_csv(csv_file, index=False, encoding="utf-8")

                st.session_state.show_msg = True
                st.session_state.msg_text = "削除しました！"
                st.session_state.msg_type = "error"
                
                st.session_state.confirm_delete = False
                st.rerun()

        with c2:
            if cc2.button("キャンセル"):
                st.session_state.confirm_delete = False
                st.rerun()
    
st.caption("© 2025 b-mon Analyzer | Streamlit + Matplotlib + Seaborn")