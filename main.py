import streamlit as st
import requests
from dataclasses import dataclass

API_URL = "https://med-protocols-ai-main.azurewebsites.net/ai"


# --- Cole seu resumo aqui (ou use st.secrets["CHATBOT_SUMMARY"]) ---
CHATBOT_SUMMARY = """
Integrating Clinical Guidelines and Genomic Data with AI: 
Towards Adaptive RAG in Healthcare

Jean Paes Landim de Lucena1, Patrick Terrematte ¹,²

¹. Postgraduate Program in Bioinformatics, Bioinformatics Multidisciplinary Environment – BioME, Universidade Federal do Rio Grande do Norte – UFRN.

². Metropole Digital Institute, UFRN.

The healthcare workflow demands the analysis of vast volumes of information, including medical records, laboratory results, and genomic data. The availability of such data grows daily, often overwhelming professionals tasked with aligning clinical and laboratory inputs with established protocols and guidelines to generate effective outputs for individualized diagnostic and therapeutic propaedeutics, tailored to the specific clinical context. In this scenario, tools based on large language models (LLMs) enable the handling of genomic data complexity and support clinical reasoning by optimizing information triage within an evidence-based practice framework. These tools aid in generating differential diagnoses and recommending personalized treatments. Within precision medicine, genomic data analysis facilitates the application of personalized therapies and preventive strategies. However, interpreting genomic data remains challenging, even for specialized professionals. Generative AI and large language models can assist in analyzing genetic variants and diseases, improving diagnostic accuracy and enhancing physician-patient communication. This project will present an API infrastructure based on intelligent agents implemented in LangGraph, utilizing an adaptive and self-corrective strategy via Retrieval-Augmented Generation (Adaptive RAG). The system employs the Llama 3.1 (70B) LLM model, with vectorized tokens stored in ChromaDB and metrics managed in LangSmith. The objective is to support clinical decision-making by integrating patient data with the Brazilian Ministry of Health’s Clinical Protocols and Therapeutic Guidelines (PCDT), alongside continuously updated genomic data from the Ensembl Variation API. This infrastructure aims to enhance diagnostic propaedeutics across healthcare tiers and enable precise, individualized clinical follow-up, particularly in resource-limited settings. As a project outcome, we will demonstrate a proof-of-concept chatbot addressing queries related to Type 2 Diabetes Mellitus PCDT guidelines and corresponding genetic testing options available in MalaCards.This infrastructure is under construction, and the results reported here reflect preliminary work in progress.

Keywords: 
Multi-Agent Systems. Generative AI. Large Language Models. Precision Medicine.
"""


class Message:
    content: str
    userName: str
    isChatbot: bool

    def __init__(self, content, userName="User", isChatbot=False):
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
        st.error("Error on obtaining response message.")

    st.session_state.waitingResponse = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "waitingResponse" not in st.session_state:
    st.session_state.waitingResponse = False

st.set_page_config(page_title="Chatbot")
st.title("Med Protocols Chat 💬")


# --- Boas-vindas com logo + resumo (só na primeira visita) ---
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.image("asset/logo.png", width=80)  # mantenha logo.png no diretório do app
        st.markdown("**Welcome!**")
        st.write("This chatbot integrates clinical guidelines with genomic data through AI.")
        st.write("It uses large language models and adaptive RAG to support healthcare decision-making.")
        st.write("Our proof-of-concept focuses on Type 2 Diabetes Mellitus and related genetic testing.")
        st.write("The system aims to improve precision medicine, even in resource-limited settings.")
        with st.expander("ℹ️ About this assistant."):
            st.markdown(CHATBOT_SUMMARY.strip() or "_Sem resumo definido._")
    st.session_state.messages.append(
        Message("Welcome! This chatbot integrates clinical guidelines with genomic data through AI.", isChatbot=True, userName="Bot")
    )

for message in st.session_state.messages:
    st.chat_message("assistant" if message.isChatbot else "user").write(message.content)


if userPrompt := st.chat_input(disabled=st.session_state.waitingResponse, placeholder="Ask me something..."):
    print(f"User prompt: {userPrompt}")
    st.chat_message("user").write(userPrompt)
    st.session_state.messages.append(Message(userPrompt, isChatbot=False, userName="User"))
    st.session_state.waitingResponse = True
    params = {"query": userPrompt, "user_id": 1}
    requests.get(API_URL, params=params, hooks={"response": [HandleChatbotResponse]})
