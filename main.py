import streamlit as st
import pandas as pd
import google.generativeai as genai
import json

# --- 1. 頁面與模型配置 ---
st.set_page_config(page_title="AI 全方位健康顧問", layout="wide", page_icon="🥗")

# 安全讀取 API Key (部署到 Cloud 時請在 Secrets 設定)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 使用 2026 年推薦的免費預覽版模型
    model = genai.GenerativeModel('gemini-3-flash-preview')
else:
    st.warning("未偵測到 API Key，AI 分析功能將受限。")

# --- 2. 初始化 Session State ---
if 'daily_logs' not in st.session_state:
    st.session_state.daily_logs = []

# --- 3. 側邊欄：進階目標與即時看板 ---
with st.sidebar:
    st.header("🎯 每日營養目標")
    t_cal = st.number_input("熱量 (kcal)", value=2000, step=100)
    t_pro = st.number_input("蛋白質 (g)", value=60, step=5)
    t_sodium = st.number_input("鈉含量 (mg)", value=2400, step=100)
    t_sugar = st.number_input("糖分 (g)", value=50, step=5)
    t_fiber = st.number_input("膳食纖維 (g)", value=25, step=1)
    
    st.divider()
    st.header("📊 今日累計進度")
    
    if st.session_state.daily_logs:
        df = pd.DataFrame(st.session_state.daily_logs)
        
        def show_metric(label, current, target, unit, inverse=False):
            diff = target - current
            # 鈉、糖、熱量超過為紅；纖維、蛋白不足為紅
            is_bad = diff < 0 if not inverse else diff > 0
            color = "inverse" if is_bad else "normal"
            st.metric(label, f"{current:.1f} {unit}", delta=f"{diff:.1f} 剩餘", delta_color=color)

        show_metric("🔥 熱量", df['熱量(kcal)'].sum(), t_cal, "kcal")
        show_metric("🧂 鈉", df['鈉(mg)'].sum(), t_sodium, "mg")
        show_metric("🍭 糖", df['糖(g)'].sum(), t_sugar, "g")
        show_metric("🥬 纖維", df['纖維(g)'].sum(), t_fiber, "g", inverse=True)
        st.progress(min(df['熱量(kcal)'].sum()/t_cal, 1.0))
    else:
        st.info("請新增數據開始追蹤")

# --- 4. 主頁面：功能區 ---
st.title("🥗 AI 全方位健康助手")

# --- 核心模式切換 (開發測試用) ---
tab1, tab2 = st.tabs(["📸 拍照紀錄", "🧪 模擬測試模式"])

with tab1:
    st.info("相機功能已預備，串接 API 後即可使用")
    # cam_file = st.camera_input("拍照記錄這一餐")
    # if cam_file:
    #     st.write("AI 辨識邏輯將在此執行...")

with tab2:
    st.write("點擊下方典型範例，測試數據累計與健康建議邏輯：")
    col1, col2, col3 = st.columns(3)
    
    # 模擬精密健康數據
    mocks = {
        "藜麥鮭魚健身餐": {"cal": 520, "pro": 38, "sugar": 2, "fiber": 9, "sodium": 480},
        "日式豚骨拉麵": {"cal": 880, "pro": 22, "sugar": 6, "fiber": 2, "sodium": 2900},
        "珍珠奶茶 (大)": {"cal": 650, "pro": 3, "sugar": 65, "fiber": 0.5, "sodium": 120}
    }

    def add_mock(name):
        d = mocks[name]
        st.session_state.daily_logs.append({
            "時間": pd.Timestamp.now().strftime("%H:%M"),
            "食物": name, "熱量(kcal)": d["cal"], "蛋白質(g)": d["pro"],
            "糖(g)": d["sugar"], "纖維(g)": d["fiber"], "鈉(mg)": d["sodium"]
        })
        st.rerun()

    with col1:
        st.markdown("🟢 **優質高纖**\n鮭魚、藜麥、花椰菜")
        if st.button("加入：健身餐"): add_mock("藜麥鮭魚健身餐")
    with col2:
        st.markdown("🔴 **高鈉警告**\n濃郁湯頭、叉燒、麵條")
        if st.button("加入：豚骨拉麵"): add_mock("日式豚骨拉麵")
    with col3:
        st.markdown("🟡 **高糖陷阱**\n黑糖珍珠、全糖奶茶")
        if st.button("加入：珍珠奶茶"): add_mock("珍珠奶茶 (大)")

# --- 5. 數據紀錄表 ---
st.divider()
st.subheader("📝 今日飲食清單")
if st.session_state.daily_logs:
    df_logs = pd.DataFrame(st.session_state.daily_logs)
    edited_df = st.data_editor(df_logs, use_container_width=True)
    
    c1, c2, _ = st.columns([1,1,2])
    if c1.button("💾 儲存修改內容"):
        st.session_state.daily_logs = edited_df.to_dict('records')
        st.rerun()
    if c2.button("🗑️ 清空所有數據"):
        st.session_state.daily_logs = []
        st.rerun()

    # --- 6. AI 動態健康診斷系統 ---
    st.divider()
    st.subheader("🤖 AI 營養師深度診斷")
    if st.button("🪄 針對今日表現生成 AI 建議", type="primary"):
        with st.spinner("AI 正在分析您的健康趨勢..."):
            summary = {
                "總熱量": df_logs['熱量(kcal)'].sum(),
                "總鈉量": df_logs['鈉(mg)'].sum(),
                "總糖量": df_logs['糖(g)'].sum(),
                "總纖維": df_logs['纖維(g)'].sum()
            }
            
            prompt = f"""
            你是一位專業且直言不諱的營養師。
            今日數據：{summary}
            今日目標：熱量{t_cal}, 鈉{t_sodium}, 糖{t_sugar}, 纖維{t_fiber}。
            
            請根據以上數據：
            1. 分析哪項參數最危險並說明對健康的即時影響（如水腫、血糖波動）。
            2. 稱讚一個做得好的地方。
            3. 給予明天第一餐的「具體補救建議」。
            4. 語氣要專業、生動，可以使用 Emoji。
            請用繁體中文回答。
            """
            try:
                response = model.generate_content(prompt)
                st.info("營養師碎碎念：")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"AI 罷工中，請稍後再試: {e}")
else:
    st.write("目前尚無數據可供分析。")
