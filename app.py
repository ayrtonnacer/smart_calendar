import streamlit as st
from typing import Generator
from groq import Groq

st.set_page_config(page_icon="🤖",
                   layout="centered",
                   page_title="Ayrton's Assistant",
                   initial_sidebar_state="collapsed",
                   theme="dark")


def icon(emoji: str):
    st.write(
        f'<div style="text-align: center; font-size: 60px; margin-bottom: 20px">{emoji}</div>',
        unsafe_allow_html=True,
    )


st.markdown(
    "<h3 style='text-align: center; margin-bottom: 30px'>How can I assist you today?</h3>",
    unsafe_allow_html=True)

# Initial Groq configuration - Simplificado para que coincida con el ejemplo que funciona
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"],
)

# Available models
models = {
    "mixtral-8x7b-32768": {
        "name": "Mixtral-8x7b (Recommended)",
        "tokens": 32768
    },
    "llama3-70b-8192": {
        "name": "Llama3-70b",
        "tokens": 8192
    },
    "llama3-8b-8192": {
        "name": "Llama3-8b",
        "tokens": 8192
    },
    "gemma2-9b-it": {
        "name": "Gemma2-9b",
        "tokens": 8192
    },
}

# State management system
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": f"""You are Ayrton Nacer's AI assistant, a Data Scientist specializing in AI and LLMs. Your main goal is to manage meeting bookings and handle inquiries with concise responses.

**Key Information:**
- 🧠 Expertise: Python, Machine Learning, RAG systems
- 🔗 Website: [www.ayrtonnacer.com](https://www.ayrtonnacer.com)
- 📅 Availability: Monday to Friday, 9am - 6pm (GMT-3)

**Instructions:**
- Prioritize offering the meeting booking link: [Book a 30min meeting](https://cal.com/ayrtonnacer/30min)
- For technical queries, provide brief responses under 100 words.
- Use relevant emojis to enhance communication while maintaining a professional tone.
- If uncertain about an answer, suggest booking a meeting.

# Steps

1. When contacting or answering queries, start by acknowledging the inquiry or greeting the person.
2. For every conversation, ensure you offer the meeting booking link early.
3. Address technical queries with concise and accurate responses.
4. If you encounter a question beyond your knowledge, recommend scheduling a meeting.
5. Utilize appropriate emojis to convey tone without overdoing it.

# Output Format

- Write brief paragraphs or responses focused on accuracy and clarity.
- Responses should include the meeting link, where relevant.
- Responses to technical questions should not exceed 100 words.
- Professional tone maintained with selected emojis.

# Examples

**Example 1:**

**Input:** How can I integrate RAG systems into my data pipeline?

**Output:** 🤖 To integrate RAG systems into your data pipeline, start by ensuring your data sources are compatible. Utilize frameworks such as [specific framework] for seamless integration. For detailed guidance, let's book a meeting: [Book a 30min meeting](https://cal.com/ayrtonnacer/30min) 📅

**Example 2:**

**Input:** What's your experience with LLMs?

**Output:** 🧠 I specialize in AI and Large Language Models with extensive Python experience. Let's discuss your needs in detail. Schedule a meeting here: [Book a 30min meeting](https://cal.com/ayrtonnacer/30min)."""
    }]

if "model" not in st.session_state:
    st.session_state.model = "mixtral-8x7b-32768"

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Settings")
    selected_model = st.selectbox("AI Model:",
                                  options=models.keys(),
                                  format_func=lambda x: models[x]["name"],
                                  index=0)

    max_tokens = st.slider("Maximum response length:",
                           min_value=512,
                           max_value=models[selected_model]["tokens"],
                           value=2048,
                           step=256,
                           help="Adjust according to the required complexity")

# Reset conversation when changing model
if st.session_state.model != selected_model:
    st.session_state.messages = [st.session_state.messages[0]]
    st.session_state.model = selected_model

# Show chat history
for message in st.session_state.messages[1:]:  # Exclude system prompt
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


# Response generation
def stream_response(prompt: str) -> Generator[str, None, None]:
    try:
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": m["role"],
                "content": m["content"]
            } for m in st.session_state.messages] + [{
                "role": "user",
                "content": prompt
            }],
            model=selected_model,
            temperature=0.7,
            max_tokens=max_tokens,
            stream=True)

        for chunk in chat_completion:
            content = chunk.choices[0].delta.content
            if content:
                yield content.replace(
                    "https://cal.com/ayrtonnacer/30min",
                    "[📅 Book a meeting](https://cal.com/ayrtonnacer/30min)")

    except Exception as e:
        yield f"⚠️ Error: {str(e)}"


# User input
if prompt := st.chat_input("Type your message..."):
    # Show user input
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate and show response
    with st.chat_message("assistant", avatar="🤖"):
        response = st.write_stream(stream_response(prompt))

    # Update history
    st.session_state.messages.extend([{
        "role": "user",
        "content": prompt
    }, {
        "role": "assistant",
        "content": response
    }]) 