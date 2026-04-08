import streamlit as st
from PIL import Image
import io

# 1. 頁面設定
st.set_page_config(page_title="手機相機測試", layout="centered")

st.title("📸 手機鏡頭調用系統")
st.write("提示：若使用手機，請確保使用 Safari 或 Chrome 並允許相機權限。")

# 2. 側邊欄：說明與設定
with st.sidebar:
    st.header("設定")
    st.info("目前的瀏覽器若支援，你會在相機畫面下方看到『切換相機』的按鈕。")

# 3. 主功能區：攝像頭元件
# st.camera_input 會自動嘗試開啟預設鏡頭
picture = st.camera_input("點擊下方按鈕拍照")

if picture:
    # 顯示成功訊息
    st.success("成功擷取影像！")
    
    # 將圖片資料轉換為 PIL 格式，方便後續處理
    img = Image.open(picture)
    
    # 4. 顯示拍到的照片
    st.image(img, caption="剛剛拍下的照片", use_column_width=True)
    
    # 5. 提供下載功能
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="下載這張照片",
        data=byte_im,
        file_name="captured_image.jpg",
        mime="image/jpeg"
    )

# 6. 底層偵錯資訊（選填）
with st.expander("查看檔案資訊"):
    if picture:
        st.write(f"檔名: {picture.name}")
        st.write(f"檔案大小: {picture.size} bytes")
    else:
        st.write("尚未拍攝任何照片")
