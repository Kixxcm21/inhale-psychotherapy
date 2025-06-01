import streamlit as st
from transformers import pipeline

# 建立對話機器人，使用 facebook/blenderbot-400M-distill 這個模型
chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")

# 在程式中用 chatbot([user_input]) 來取得回答


# 載入對話模型（會自動下載模型）
@st.cache_resource
def load_model():
    return pipeline("conversational", model="microsoft/DialoGPT-small")

chatbot = load_model()

if "history" not in st.session_state:
    st.session_state.history = []

st.title("Inhale 心理諮詢（本機版）")

user_input = st.text_input("請輸入訊息：", "")

if user_input:
    # 新增用戶訊息
    st.session_state.history.append({"role": "user", "content": user_input})

    # 用 Conversation 包裝過去對話
    conv = Conversation()
    for msg in st.session_state.history:
        if msg["role"] == "user":
            conv.add_user_input(msg["content"])
        else:
            # DialoGPT 回應
            pass

    # 取得模型回答
    result = chatbot(conv)
    bot_reply = result.generated_responses[-1]

    # 新增機器人回覆
    st.session_state.history.append({"role": "bot", "content": bot_reply})

# 顯示對話
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f"**你：** {msg['content']}")
    else:
        st.markdown(f"**Inhale：** {msg['content']}")
