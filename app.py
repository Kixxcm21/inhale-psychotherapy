import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# 載入 .env 中的 API 金鑰
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 初始化 OpenAI client（新版寫法）
client = OpenAI(api_key=api_key)

# 初始化對話紀錄
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一個溫暖且具有療癒感的心理輔助者，擅長傾聽並用理解與支持的語氣回應使用者。請用繁體中文回答。"}
    ]

st.set_page_config(page_title="Inhale 心理諮詢", page_icon="🌿")

st.title("🫧 Inhale 心理諮詢")
st.write("🌱 有時候，把心裡的話說出來，就已經是一種療癒。")

# 顯示對話紀錄
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

# 輸入框
user_input = st.chat_input("現在的你，想談談什麼呢？")

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
    except Exception as e:
        st.error("⚠️ 發生錯誤：" + str(e))
