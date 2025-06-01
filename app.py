import streamlit as st
from huggingface_hub import InferenceClient

# 設定 Hugging Face API 密鑰
HF_API_TOKEN = st.secrets["HF_API_TOKEN"]  # 確保你已在 Streamlit secrets 中設定
client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=HF_API_TOKEN)

st.set_page_config(page_title="Inhale 心理諮詢", page_icon="🫧")
st.title("🫧 Inhale 心理諮詢")
st.caption("空氣中溫稔的聲音。你可以聊聊心事。")

# 保留對話紀錄
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "你是一名溫柔、應志、有心理指導能力的助理諮詢師，會以感同、接納的話語回應使用者，給予您沉靜及安慰。"}
    ]

# 顯示過去的話題
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 接收新的用戶話題
if user_input := st.chat_input("我有點想聊聊..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = client.text_generation(
            prompt=f"<|system|>{st.session_state.messages[0]['content']}\n<|user|>{user_input}\n<|assistant|>",
            max_new_tokens=256,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
        )
        assistant_reply = response.strip()
        st.markdown(assistant_reply)
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})


