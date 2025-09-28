import streamlit as st
import requests
import json
import re
from dataclasses import dataclass

API_URL = "https://med-protocols-ai-main.azurewebsites.net/ai"

# --- helper: render markdown preservando \n ---
def render_markdown_preserving_newlines(md: str):
    """
    Converte quebras simples \n em quebras de linha do Markdown ("  \n"),
    mantendo \n\n como parágrafo e preservando blocos de código ```...```.
    """
    parts = re.split(r"(```[\s\S]*?```)", md)  # separa blocos de código
    for i in range(0, len(parts), 2):  # só processa trechos fora de ```
        segment = parts[i]
        # substitui \n simples por "  \n" (não toca em \n\n)
        segment = re.sub(r"(?<!\n)\n(?!\n)", "  \n", segment)
        parts[i] = segment
    st.markdown("".join(parts))

@dataclass
class Message:
    content: str
    userName: str = "User"
    isChatbot: bool = False

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

def HandleChatbotResponse(response, *args, **kwargs):
    try:
        response.raise_for_status()
        raw = response.text or ""
        # 1) tentar decodificar como JSON (muitos backends retornam "string" com \n)
        try:
            decoded = json.loads(raw)
            # se veio {"answer": "..."} pega campo; se veio "..." já é string
            if isinstance(decoded, dict):
                message = decoded.get("answer") or decoded.get("message") or decoded.get("text") or raw
            else:
                message = str(decoded)
        except json.JSONDecodeError:
            # fallback: texto puro
            message = raw

        # 2) guarda a versão bruta no histórico
        st.session_state.messages.append(Message(message, isChatbot=True, userName="Chatbot"))

        # 3) exibe com quebras de linha preservadas (Markdown friendly)
        with st.chat_message("assistant"):
            render_markdown_preserving_newlines(message)

    except requests.RequestException:
        st.error("Error on obtaining response message.")
    finally:
        st.session_state.waitingResponse = False

# --- estado
if "messages" not in st.session_state:
    st.session_state.messages = []
if "waitingResponse" not in st.session_state:
    st.session_state.waitingResponse = False

st.set_page_config(page_title="Chatbot")
st.title("Med Protocols Chat 💬")

# --- Boas-vindas com logo + resumo (só na primeira visita) ---
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.image("asset/logo.png", width=80)
        st.markdown(
            "**Welcome!**  \n"
            "This chatbot integrates clinical guidelines with genomic data through AI.  \n"
            "It uses large language models and adaptive RAG to support healthcare decision-making.  \n"
            "Our proof-of-concept focuses on Type 2 Diabetes Mellitus and related genetic testing.  \n"
            "The system aims to improve precision medicine, even in resource-limited settings."
        )
        with st.expander("ℹ️ About this assistant."):
            render_markdown_preserving_newlines(CHATBOT_SUMMARY.strip() or "_No summary defined._")
    st.session_state.messages.append(
        Message("Welcome! This chatbot integrates clinical guidelines with genomic data through AI.", isChatbot=True, userName="Bot")
    )

# --- histórico (usar markdown com preservação de \n)
for message in st.session_state.messages:
    with st.chat_message("assistant" if message.isChatbot else "user"):
        render_markdown_preserving_newlines(message.content)

# --- input
if userPrompt := st.chat_input(disabled=st.session_state.waitingResponse, placeholder="Ask me something..."):
    st.chat_message("user").write(userPrompt)
    st.session_state.messages.append(Message(userPrompt, isChatbot=False, userName="User"))
    st.session_state.waitingResponse = True
    params = {"query": userPrompt, "user_id": 1}
    requests.get(API_URL, params=params, hooks={"response": [HandleChatbotResponse]})
