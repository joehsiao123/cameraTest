import streamlit as st
import pandas as pd # 簡化寫法

# --- 1. 頁面配置 ---
st.set_page_config(page_title="全方位健康助手", layout="wide")

# --- 2. 初始化 Session State ---
if 'daily_logs' not in st.session_state:
    st.session_state.daily_logs = []

# --- 3. 側邊欄：進階健康目標設定 ---
with st.sidebar:
    st.header("🎯 進階健康目標")
    target_cal = st.number_input("熱量 (kcal)", value=2000)
    
    with st.expander("微量與細項設定"):
        target_pro = st.number_input("蛋白質 (g)", value=60)
        target_fiber = st.number_input("膳食纖維 (g)", value=25, help="建議每日攝取 25-35g")
        target_sodium = st.number_input("鈉含量 (mg)", value=2400, help="WHO 建議每日不超過 2400mg")
        target_sugar = st.number_input("添加糖 (g)", value=50, help="建議不超過總熱量的 10%")
        target_sat_fat = st.number_input("飽和脂肪 (g)", value=20)

    st.divider()
    st.header("📊 今日達成進度")
    
    if st.session_state.daily_logs:
        df = pd.DataFrame(st.session_state.daily_logs)
        
        # 定義指標顯示函式
        def health_metric(label, current, target, unit, inverse=False):
            diff = target - current
            # 對於鈉、糖、飽和脂肪，超過目標（diff < 0）應該顯示紅色警告
            is_warning = diff < 0 if not inverse else diff > 0
            color = "inverse" if is_warning else "normal"
            st.metric(label, f"{current:.1f} {unit}", delta=f"{diff:.1f} 剩餘", delta_color=color)

        health_metric("🔥 總熱量", df['熱量(kcal)'].sum(), target_cal, "kcal")
        health_metric("🧂 鈉含量", df['鈉(mg)'].sum(), target_sodium, "mg")
        health_metric("🍭 總糖分", df['糖(g)'].sum(), target_sugar, "g")
        health_metric("🥬 纖維質", df['纖維(g)'].sum(), target_fiber, "g", inverse=True)
        
        st.progress(min(df['熱量(kcal)'].sum()/target_cal, 1.0))
    else:
        st.info("尚無數據")

# --- 4. 主頁面：精心設計的健康範例 ---
st.title("🛡️ 專業健康管理模式 (模擬)")
st.write("我們設計了三種代表性的健康/非健康餐飲，請觀察參數變化：")

col1, col2, col3 = st.columns(3)

# 模擬高規格健康數據
mock_data = {
    "藜麥鮭魚健身餐": {"cal": 550, "pro": 35, "carb": 45, "fat": 22, "fiber": 8.5, "sodium": 450, "sugar": 2},
    "日式拉麵 (豚骨)": {"cal": 850, "pro": 25, "carb": 85, "fat": 38, "fiber": 2.0, "sodium": 2800, "sugar": 5},
    "超商雞肉飯糰": {"cal": 220, "pro": 5, "carb": 42, "fat": 3, "fiber": 1.0, "sodium": 650, "sugar": 1}
}

def add_entry(name):
    d = mock_data[name]
    st.session_state.daily_logs.append({
        "時間": "12:00", "食物": name, 
        "熱量(kcal)": d["cal"], "蛋白質(g)": d["pro"], 
        "糖(g)": d["sugar"], "纖維(g)": d["fiber"], "鈉(mg)": d["sodium"]
    })
    st.rerun()

with col1:
    st.subheader("🟢 優質選擇")
    st.write("**藜麥鮭魚餐**\n高纖維、低鈉、優質蛋白")
    if st.button("加入紀錄", key="h1"): add_entry("藜麥鮭魚健身餐")

with col2:
    st.subheader("🔴 隱形殺手")
    st.write("**日式豚骨拉麵**\n**鈉含量極高**，幾乎一次超標")
    if st.button("加入紀錄", key="h2"): add_entry("日式拉麵 (豚骨)")

with col3:
    st.subheader("🟡 便利選擇")
    st.write("**雞肉飯糰**\n中規中矩，但纖維質明顯不足")
    if st.button("加入紀錄", key="h3"): add_entry("超商雞肉飯糰")

# --- 5. 數據分析報表 ---
st.divider()
st.subheader("📝 詳細數據清單")
if st.session_state.daily_logs:
    df_logs = pd.DataFrame(st.session_state.daily_logs)
    st.data_editor(df_logs, use_container_width=True)
    
    # 額外的健康洞察
    st.subheader("🔍 AI 健康建議")
    total_sodium = df_logs['鈉(mg)'].sum()
    if total_sodium > 2400:
        st.warning("⚠️ 今日鈉攝取已超標！建議多喝水，並補充含鉀食物（如香蕉、菠菜）幫助排鈉。")
    
    total_fiber = df_logs['纖維(g)'].sum()
    if total_fiber < 15:
        st.info("🥬 纖維質攝取偏低，下午茶可以考慮吃一份水果或一小把堅果。")
