import streamlit as st
import openai
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Medical AI Bot",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize OpenAI client
def initialize_openai():
    """Initialize OpenAI client with API key"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables.")
        st.info("Create a .env file with your OpenAI API key: OPENAI_API_KEY=your_key_here")
        return None
    
    openai.api_key = api_key
    return openai

# Initialize session state
def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system", 
                "content": """You are a helpful medical AI assistant. You provide general medical information and guidance, but you are not a replacement for professional medical advice. Always remind users to consult with healthcare professionals for serious health concerns. Be empathetic, accurate, and helpful while maintaining appropriate medical disclaimers."""
            }
        ]
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False

def get_ai_response(messages, model="gpt-3.5-turbo"):
    """Get response from OpenAI API"""
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main application function"""
    
    # Initialize
    client = initialize_openai()
    initialize_session_state()
    
    # Header
    st.title("🩺 Medical AI Bot")
    st.markdown("*Your AI-powered medical information assistant*")
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.info(
            "This Medical AI Bot provides general medical information and guidance. "
            "**Always consult with qualified healthcare professionals for medical advice, "
            "diagnosis, or treatment.**"
        )
        
        st.header("⚙️ Settings")
        model_choice = st.selectbox(
            "AI Model",
            ["gpt-3.5-turbo", "gpt-4"],
            help="Choose the AI model for responses"
        )
        
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = [st.session_state.messages[0]]  # Keep system message
            st.session_state.conversation_started = False
            st.rerun()
    
    # Main content
    if not client:
        st.stop()
    
    # Display conversation
    if st.session_state.conversation_started:
        st.subheader("💬 Conversation")
        
        # Display messages (skip system message)
        for message in st.session_state.messages[1:]:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask me about medical topics, symptoms, or health concerns...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.conversation_started = True
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get and display AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_ai_response(st.session_state.messages, model_choice)
                st.write(response)
        
        # Add AI response to messages
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to update the display
        st.rerun()
    
    # Welcome message
    if not st.session_state.conversation_started:
        st.subheader("👋 Welcome to Medical AI Bot")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### What I can help with:
            - General medical information
            - Symptom explanations
            - Health and wellness tips
            - Medication information
            - Medical terminology
            """)
        
        with col2:
            st.markdown("""
            ### Important Disclaimers:
            - Not a substitute for professional medical advice
            - Always consult healthcare providers for diagnosis
            - Don't rely solely on AI for medical decisions
            - Seek immediate help for emergencies
            """)
        
        st.markdown("---")
        st.info("💡 **Tip**: Start by typing your medical question or health concern in the chat box below!")

if __name__ == "__main__":
    main()