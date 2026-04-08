import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.title("強制調用 iPhone 後鏡頭")

# 定義攝像頭約束條件
# "environment" 代表後鏡頭，"user" 代表前鏡頭
RTC_CONFIGURATION = {
    "video": {
        "facingMode": "environment",
    }
}

webrtc_streamer(
    key="back-camera",
    rtc_configuration=None, # 若不需要 STUN/TURN 伺服器則設為 None
    media_stream_constraints=RTC_CONFIGURATION
)
