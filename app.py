import streamlit as st
import openai
import os
from dotenv import load_dotenv

# 載入 .env 檔案中的 API 金鑰
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 頁面標題
st.set_page_config(page_title="Inhale 心理諮詢", page_icon="🫧")
st.title("🫧 Inhale｜AI 心理協談")

# 初始化對話紀錄
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一位溫柔、理解且理性的心理師，會用理解與陪伴的方式，協助使用者探索他的情緒與問題。請用繁體中文回答。"}
    ]

# 顯示聊天紀錄
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 使用者輸入
if prompt := st.chat_input("請放心地說說你此刻的心情⋯⋯"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 呼叫 OpenAI API 並產生回應
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            api_key=api_key  # 加上這行才能正確使用你 .env 裡的金鑰
        )
        reply = response.choices[0].message.content
        st.markdown(reply)

    # 儲存 assistant 回應
    st.session_state.messages.append({"role": "assistant", "content": reply})
