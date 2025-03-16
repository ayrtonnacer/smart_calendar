A Streamlit application that uses Groq's API to power an AI assistant for managing bookings and handling technical inquiries.

## Features
- Uses multiple LLM models including Mixtral, Llama3, and Gemma2
- Configurable response length
- Streaming responses
- Professional, emoji-enhanced communication

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set up a virtual environment (optional but recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
1. Add your Groq API key to `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your-groq-api-key-here"
```
You can get a Groq API key by signing up at [https://console.groq.com/](https://console.groq.com/)

### 5. Run the application
```bash
streamlit run app.py
```

## Usage
1. The application will start on `http://localhost:8501`
2. Select a model from the sidebar
3. Adjust the maximum response length as needed
4. Type your message in the chat input
5. Receive AI-generated responses with meeting booking links

## Models Available
- Mixtral-8x7b (32K context window)
- Llama3-70b (8K context window)
- Llama3-8b (8K context window)
- Gemma2-9b (8K context window) 