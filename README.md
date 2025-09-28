# 🩺 Medical AI Bot

A comprehensive medical AI assistant built with Streamlit and OpenAI's GPT models. This bot provides general medical information, symptom explanations, and health guidance while maintaining appropriate medical disclaimers.

## ✨ Features

- **Interactive Chat Interface**: User-friendly conversation interface for medical queries
- **AI-Powered Responses**: Utilizes OpenAI's GPT models for intelligent medical information
- **Model Selection**: Choose between GPT-3.5-turbo and GPT-4 models
- **Medical Disclaimers**: Built-in safety reminders about professional medical advice
- **Conversation Management**: Clear conversation history and start fresh discussions
- **Responsive Design**: Clean, modern UI optimized for medical consultations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/terrematte/medical-dna-bot.git
   cd medical-dna-bot
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Configure your API key**
   - Edit the `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

4. **Start the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - Navigate to `http://localhost:8501`

### Manual Installation

If you prefer manual setup:

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env file with your OpenAI API key
# Then run the app
streamlit run app.py
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required: Your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Model selection (default: gpt-3.5-turbo)
OPENAI_MODEL=gpt-3.5-turbo
```

### Supported Models
- `gpt-3.5-turbo` (default, faster and more cost-effective)
- `gpt-4` (more advanced but slower and more expensive)

## 📱 Usage

1. **Start a Conversation**: Type your medical question in the chat input
2. **Get AI Responses**: The bot provides informative medical guidance
3. **Change Models**: Use the sidebar to switch between AI models
4. **Clear History**: Reset the conversation anytime using the sidebar button

### Example Queries
- "What are the symptoms of diabetes?"
- "How can I manage high blood pressure?"
- "What should I know about vitamin D deficiency?"
- "Explain the difference between bacterial and viral infections"

## ⚠️ Important Disclaimers

- **Not a Medical Professional**: This bot provides general information only
- **Consult Healthcare Providers**: Always seek professional medical advice for diagnosis and treatment
- **Emergency Situations**: Contact emergency services immediately for urgent medical issues
- **Personal Health Decisions**: Do not rely solely on AI for important health decisions

## 🛠️ Development

### Project Structure
```
medical-dna-bot/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── setup.py           # Setup script
├── .env.example       # Environment template
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

### Running in Development Mode
```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
streamlit run app.py --server.runOnSave true
```

## 📋 Requirements

- streamlit>=1.28.0
- openai>=1.0.0
- python-dotenv>=1.0.0
- requests>=2.31.0

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check that your OpenAI API key is correctly set in the `.env` file
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. Verify your Python version is 3.8 or higher
4. Check the Streamlit documentation for deployment issues

## 🔒 Privacy & Security

- API keys are stored locally in `.env` files (not committed to version control)
- Conversations are not logged or stored permanently
- All medical queries are processed through OpenAI's secure API

---

**Disclaimer**: This tool is for educational and informational purposes only. It is not intended to replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns.