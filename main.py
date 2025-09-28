import streamlit as st
import requests
class Message:
    content: str
    userName: str
    isChatbot: bool

    def __init__(self, content, userName="Usuário", isChatbot=False):
        self.content = content
        self.userName = userName
        self.isChatbot = isChatbot

def HandleChatbotResponse(response, *args, **kwargs):
    if response.status_code == 200:
        print(f"Response received: {response.text}")
        message = response.text
        if(message[0] == '"'):
            message = message[1:-1]

        if(message[-1] == '"'):
            message = message[:-1]
        st.session_state.messages.append(Message(message, isChatbot=True, userName="Chatbot"))
        st.chat_message("assistant").write(message)
    else:
        st.error("Erro ao obter resposta do chatbot.")

    st.session_state.waitingResponse = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "waitingResponse" not in st.session_state:
    st.session_state.waitingResponse = False

st.title("PCDT Bot")

for message in st.session_state.messages:
    st.chat_message("assistant" if message.isChatbot else "user").write(message.content)


if userPrompt := st.chat_input(disabled=st.session_state.waitingResponse, placeholder="Digite sua mensagem aqui..."):
    print(f"User prompt: {userPrompt}")
    st.chat_message("user").write(userPrompt)
    st.session_state.messages.append(Message(userPrompt, isChatbot=False, userName="Usuário"))
    st.session_state.waitingResponse = True
    requests.get("https://med-protocols-ai-main.azurewebsites.net/ai", params={"query": userPrompt, "user_id": 1}, hooks={"response": [HandleChatbotResponse]})
