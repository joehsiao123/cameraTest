import streamlit as st
import pandas as pd

# --- 1. 頁面配置 ---
st.set_page_config(page_title="營養追蹤邏輯測試", layout="wide")

# --- 2. 初始化 Session State ---
if 'daily_logs' not in st.session_state:
    st.session_state.daily_logs = []

# --- 3. 側邊欄：目標設定與差距分析 ---
with st.sidebar:
    st.header("🎯 每日營養目標")
    target_cal = st.number_input("熱量目標 (kcal)", value=2000)
    target_pro = st.number_input("蛋白質目標 (g)", value=60)
    target_carb = st.number_input("碳水目標 (g)", value=250)
    target_fat = st.number_input("脂肪目標 (g)", value=55)
    
    st.divider()
    st.header("📊 達成進度分析")
    
    if st.session_state.daily_logs:
        df = pd.DataFrame(st.session_state.daily_logs)
        curr_cal = df['熱量(kcal)'].sum()
        curr_pro = df['蛋白質(g)'].sum()
        curr_carb = df['碳水(g)'].sum()
        curr_fat = df['脂肪(g)'].sum()

        # 熱量剩餘指標
        rem_cal = target_cal - curr_cal
        st.metric("熱量剩餘 (kcal)", f"{rem_cal:.0f}", delta=f"{rem_cal}", delta_color="normal" if rem_cal >= 0 else "inverse")
        
        # 進度條
        st.progress(min(curr_cal/target_cal, 1.0), text=f"熱量達成率: {int(curr_cal/target_cal*100)}%")

        # 詳細差距顯示
        def show_status(label, current, target, unit):
            diff = target - current
            color = "green" if diff >= 0 else "red"
            st.markdown(f"{label}: **{current:.1f}** / {target} {unit}  \n(剩餘: :{color}[{diff:.1f}])")

        st.write("---")
        show_status("🥩 蛋白質", curr_pro, target_pro, "g")
        show_status("🍞 碳水", curr_carb, target_carb, "g")
        show_status("🥑 脂肪", curr_fat, target_fat, "g")
    else:
        st.info("請點擊右側按鈕加入測試數據")

# --- 4. 主頁面：固定範例測試 ---
st.title("🧪 營養追蹤邏輯測試模式")
st.info("目前已暫時註解相機功能，請使用下方預設範例進行測試。")

# --- 註解掉的相機功能 ---
# img_file = st.camera_input("拍照紀錄") 
# -------------------------

st.subheader("💡 點擊下方範例食物模擬紀錄")

col1, col2, col3 = st.columns(3)

# 預設三組測試數據
mock_data = {
    "美式大早餐": {"cal": 850, "pro": 35, "carb": 45, "fat": 58},
    "舒肥雞肉沙拉": {"cal": 320, "pro": 28, "carb": 12, "fat": 15},
    "大杯珍珠奶茶": {"cal": 650, "pro": 3, "carb": 92, "fat": 30}
}

with col1:
    st.image("https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=400", caption="培根、蛋、吐司")
    if st.button("加入：美式大早餐"):
        d = mock_data["美式大早餐"]
        st.session_state.daily_logs.append({"時間": "08:30", "食物": "美式大早餐", "熱量(kcal)": d["cal"], "蛋白質(g)": d["pro"], "碳水(g)": d["carb"], "脂肪(g)": d["fat"]})
        st.rerun()

with col2:
    st.image("https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400", caption="低卡雞肉、生菜")
    if st.button("加入：舒肥雞肉沙拉"):
        d = mock_data["舒肥雞肉沙拉"]
        st.session_state.daily_logs.append({"時間": "12:15", "食物": "舒肥雞肉沙拉", "熱量(kcal)": d["cal"], "蛋白質(g)": d["pro"], "碳水(g)": d["carb"], "脂肪(g)": d["fat"]})
        st.rerun()

with col3:
    st.image("https://images.unsplash.com/photo-1572049285918-6c8430b56877?w=400", caption="高糖、高碳水")
    if st.button("加入：大杯珍珠奶茶"):
        d = mock_data["大杯珍珠奶茶"]
        st.session_state.daily_logs.append({"時間": "15:30", "食物": "大杯珍珠奶茶", "熱量(kcal)": d["cal"], "蛋白質(g)": d["pro"], "碳水(g)": d["carb"], "脂肪(g)": d["fat"]})
        st.rerun()

# --- 5. 數據表格 ---
st.divider()
st.subheader("📝 今日飲食清單 (可手動微調)")
if st.session_state.daily_logs:
    df_logs = pd.DataFrame(st.session_state.daily_logs)
    edited_df = st.data_editor(df_logs, use_container_width=True)
    
    # 點擊按鈕同步手動編輯後的結果
    if st.button("儲存修改並更新看板"):
        st.session_state.daily_logs = edited_df.to_dict('records')
        st.rerun()
        
    if st.button("🗑️ 全部清空"):
        st.session_state.daily_logs = []
        st.rerun()
else:
    st.write("尚未新增任何測試數據。")
