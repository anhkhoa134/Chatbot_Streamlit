import streamlit as st
import requests

# Thiết lập URL API LM Studio
API_URL = "http://100.65.5.56:1234/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json"
}
MODEL_NAME = "gemma-2-9b-it"

# Hàm gửi message tới LM Studio
def chat_with_bot(messages):
    data = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500
    }
    response = requests.post(API_URL, headers=HEADERS, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Có lỗi xảy ra khi kết nối đến LM Studio."

# Giao diện Streamlit
st.title("🦙 Chatbot LM Studio (Gemma-2-9B-IT)")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Bạn đang trò chuyện với chatbot LM Studio!"}
    ]

# Hiển thị các tin nhắn trước đó
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Ô nhập liệu
user_input = st.chat_input("Nhập tin nhắn...")

if user_input:
    # Thêm message người dùng vào session
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Hiển thị tin nhắn người dùng
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gửi và hiển thị phản hồi từ chatbot
    with st.chat_message("assistant"):
        response = chat_with_bot(st.session_state.messages)
        st.markdown(response)

    # Thêm tin nhắn chatbot vào session
    st.session_state.messages.append({"role": "assistant", "content": response})
