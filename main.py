import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 頁面配置 ---
st.set_page_config(page_title="AI 食物營養師", page_icon="🥗")

# --- 安全讀取 API Key ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("請在 Streamlit Secrets 中設定 GEMINI_API_KEY")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- 模型初始化 (解決 404 問題) ---
def get_model():
    # 優先嘗試最新版本，如果失敗則自動尋找可用模型
    try:
        model = genai.GenerativeModel('gemini-3-flash-preview')
        return model
    except:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # 尋找名稱包含 flash 的模型
        flash_models = [m for m in available_models if "flash" in m]
        target_model = flash_models[0] if flash_models else available_models[0]
        return genai.GenerativeModel(target_model)

model = get_model()

# --- UI 介面 ---
st.title("🥗 AI 食物組成與營養分析")
st.write("請使用手機拍照或上傳圖片，讓 AI 分析營養成分。")

# 側邊欄顯示偵錯資訊（選用）
with st.sidebar:
    st.header("系統資訊")
    st.write(f"當前模型: `{model.model_name}`")

# --- 核心功能：相機輸入 ---
img_file = st.camera_input("📸 對準食物拍照")

if img_file:
    # 讀取並顯示圖片
    img = Image.open(img_file)
    st.image(img, caption="分析中...", use_column_width=True)

    # 按鈕觸發分析
    if st.button("開始分析營養成分", type="primary"):
        with st.spinner('AI 正在思考中...'):
            try:
                # 提示詞 (Prompt)
                prompt = """
                你是一位專業的營養師。請根據這張圖片執行以下任務：
                1. 辨識圖中所有的食物組成（食材）。
                2. 估算總熱量(kcal)及三大營養素（蛋白質、脂肪、碳水化合物）。
                3. 以 Markdown 表格形式呈現分析結果。
                4. 針對這餐提供一句簡短的健康建議。
                請使用繁體中文回答。
                """
                
                # 發送給 Gemini
                response = model.generate_content([prompt, img])
                
                # 顯示結果
                st.subheader("📊 營養分析結果")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"分析失敗，錯誤訊息：{e}")
                st.info("提示：如果持續 404，請檢查您的 Google AI Studio 權限是否包含 Gemini 1.5 Flash。")

# --- 頁尾 ---
st.divider()
st.caption("⚠️ 注意：AI 估算數值僅供參考，實際數值可能因份量與烹飪方式而有差異。")
