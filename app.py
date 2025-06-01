iimport streamlit as st
from transformers import pipeline

st.title("Inhale 心理諮詢 - 開源模型版")

# 建立對話機器人（只建立一次）
@st.cache_resource
def load_model():
    return pipeline("conversational", model="facebook/blenderbot-400M-distill")

chatbot = load_model()

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("請輸入你的訊息：")

if user_input:
    # 把對話加入歷史，送給模型
    st.session_state.history.append(user_input)
    inputs = st.session_state.history[-1]

    # 產生回答
    response = chatbot(inputs)

    # 取得回答文字，blenderbot pipeline 會回傳一個 list 裡面包含對話物件
    bot_reply = response[0]["generated_text"]
    st.session_state.history.append(bot_reply)

    # 顯示對話歷史
    for i, msg in enumerate(st.session_state.history):
        if i % 2 == 0:
            st.markdown(f"**你:** {msg}")
        else:
            st.markdown(f"**Inhale:** {msg}")

