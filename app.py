import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# 載入 .env 中的環境變數
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 建立 OpenAI 客戶端
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Inhale 心理諮詢", page_icon="🫧")
st.title("🫧 Inhale 心理諮詢")

# 初始化對話紀錄
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一位溫暖、理解且專業的心理師，善於傾聽使用者的困擾，並引導他們探索自己的情緒與需求。請用貼近人心的方式回應對方的話語，不用給太多分析，先讓對方感受到被理解。"}
    ]

# 顯示歷史訊息
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 使用者輸入
if prompt := st.chat_input("請說說你最近的心情……"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 呼叫 OpenAI API 取得回應
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
    )
    reply = response.choices[0].message.content

    # 加入回應到對話紀錄並顯示
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
