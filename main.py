import streamlit as st
import google.generativeai as genai
from PIL import Image

# 從 Secrets 自動讀取
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AI 食物營養分析師", layout="centered")

st.title("🥗 AI 食物組成與營養分析")
st.write("請對準食物拍照，AI 將自動分析其內容物。")

# 調用相機
img_file = st.camera_input("拍照分析食物")

if img_file:
    # 讀取圖片
    img = Image.open(img_file)
    st.image(img, caption="正在分析此影像...", use_column_width=True)

    with st.spinner('AI 正在計算營養成分中...'):
        try:
            # 設定 AI 的指令
            prompt = """
            請分析這張照片中的食物。
            1. 列出所有的主要組成成份。
            2. 估計這份食物的營養標示（熱量、蛋白質、脂肪、碳水化合物、糖）。
            3. 請以 Markdown 表格形式呈現。
            4. 給予一個簡單的健康建議。
            """
            
            # 發送給 AI
            response = model.generate_content([prompt, img])
            
            # 顯示結果
            st.subheader("📊 分析結果")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"分析失敗：{e}")

# 底部提醒
st.info("💡 提示：AI 分析僅供參考，實際營養含量可能隨烹飪方式而異。")
