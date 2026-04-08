import streamlit as st
from PIL import Image

st.title("手機鏡頭調用測試")

# 調用相機元件
img_file = st.camera_input("請對準物品拍照")

if img_file:
    # 將上傳的檔案轉換為圖片物件
    img = Image.open(img_file)
    
    # 這裡可以進行圖片處理（例如 AI 辨識）
    st.image(img, caption="已拍攝的照片")
    st.write("圖片維度:", img.size)
