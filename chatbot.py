import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image

# Streamlit UI setup
st.set_page_config(page_title="Dynamic Hugging Face Chatbot", layout="wide")

# Background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://example.com/your-background-image.jpg');
        background-size: cover;
        background-position: center;
    }
    
    /* Style for buttons with hover effect */
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        border-radius: 5px;
        padding: 10px;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f4f4f9;
        border-radius: 8px;
        padding: 20px;
    }

    /* Chat bubble styling */
    .user-text {
        background-color: #0078D4;
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        max-width: 70%;
        margin-bottom: 10px;
    }
    
    .bot-text {
        background-color: #f1f1f1;
        color: #333;
        padding: 8px 15px;
        border-radius: 20px;
        max-width: 70%;
        margin-bottom: 10px;
    }

    /* Footer styling */
    footer {
        background-color: #1a1a1a;
        color: #f5f5f5;
        padding: 20px;
        text-align: center;
        border-radius: 8px;
    }

    footer p {
        margin: 5px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.title("✨ Dynamic Hugging Face Chatbot ✨")
st.markdown("**Interact with different Hugging Face models and have a fun conversation with your AI bot!**")
st.markdown("<hr>", unsafe_allow_html=True)

# Sidebar with model selection and custom settings
with st.sidebar:
    st.image('https://example.com/your-sidebar-image.jpg', width=250)  # Optional sidebar image
    st.header("Select Model & Configure")
    st.markdown("<hr>", unsafe_allow_html=True)

    # Model selection dropdown
    model_name = st.selectbox("Choose a model:", ["gpt2", "gpt2-medium", "gpt2-large", "gpt2-xl"])

    # Temperature slider for creativity
    temperature = st.slider("Set model creativity (temperature):", 0.1, 1.5, 0.7, 0.1)

    # Top-k slider for diversity of responses
    top_k = st.slider("Set top-k sampling:", 1, 100, 50, 1)

    # Max tokens slider for response length
    max_tokens = st.slider("Set max tokens for response:", 50, 500, 150, 10)

# Load the model and tokenizer dynamically based on selection
@st.cache_resource
def load_model(model_name):
    try:
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        return model, tokenizer
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

# Load the selected model
model, tokenizer = load_model(model_name)

# Initialize conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

# Function to interact with Hugging Face model
def get_hugging_face_response(prompt):
    try:
        input_ids = tokenizer.encode(prompt, return_tensors='pt')
        
        # Generate a response from the model with user-defined settings
        output = model.generate(input_ids, max_new_tokens=max_tokens, pad_token_id=tokenizer.eos_token_id, 
                                temperature=temperature, top_k=top_k, no_repeat_ngram_size=2)
        
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Return the response without the input prompt
        return response[len(prompt):].strip()
    except Exception as e:
        st.error(f"Error: {e}")
        return f"Error: {e}"

# User input field with a button for submitting
user_input = st.text_input("You:", "")

# Display the current question (user input) on the page
if user_input:
    st.markdown(f"### Your Question: {user_input}")

# Button for generating the response
bot_response = ""
if st.button("Send") and user_input:
    prompt = "\n".join(st.session_state.history) + f"\nYou: {user_input}\nBot:"
    
    if model and tokenizer:
        bot_response = get_hugging_face_response(prompt)
        st.session_state.history.append(f"You: {user_input}")
        st.session_state.history.append(f"Bot: {bot_response}")
    else:
        st.error("Failed to load model")

# Display the bot's response below the user input in a separate text box
if bot_response:
    st.text_area("Bot's Answer:", bot_response, height=150, max_chars=1000)

# Display conversation history in a panel
with st.expander("Conversation History"):
    for message in st.session_state.history:
        if message.startswith("You:"):
            st.markdown(f'<div class="user-text">{message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-text">{message}</div>', unsafe_allow_html=True)

# Option to reset the conversation
if st.button("Clear Conversation"):
    st.session_state.history.clear()
    st.experimental_rerun()

# Footer with additional information
st.markdown(
    """
    <footer>
        <p>Powered by Hugging Face and Streamlit</p>
    </footer>
    """,
    unsafe_allow_html=True
)
