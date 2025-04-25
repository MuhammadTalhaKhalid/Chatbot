# ✨ Dynamic Hugging Face Chatbot ✨

## Overview
Welcome to the **Dynamic Hugging Face Chatbot**! This application leverages Streamlit and Hugging Face's transformer models to provide an interactive AI chatbot experience. Users can engage in conversations with various pre-trained models, customize settings like creativity (temperature), response diversity (top-k sampling), and response length (max tokens).

## 🛠️ Installation

To run this project locally, follow these steps:


1. **Clone the Repository**
   ```bash
   git clone https://github.com/MuhammadTalhaKhalid/Chatbot.git
   cd Chatbot
Set Up a Virtual Environment (Optional but Recommended)

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
🚀 Usage
Run the Streamlit Application

bash
Copy
Edit
streamlit run chatbot.py
Interact with the Chatbot

Open the application in your browser.

Select a model from the sidebar.

Adjust settings like temperature, top-k sampling, and max tokens.

Enter your message and click "Send" to receive a response.

⚙️ Customization
Model Selection: Choose from GPT-2 variants (gpt2, gpt2-medium, gpt2-large, gpt2-xl).

Temperature: Control the creativity of the responses (range: 0.1 to 1.5).

Top-k Sampling: Adjust the diversity of responses (range: 1 to 100).

Max Tokens: Set the maximum length of the response (range: 50 to 500).

📦 Requirements
Ensure you have the following Python packages installed:

streamlit==1.44.1

transformers

Pillow==11.2.1

These can be installed via:

bash
Copy
Edit
pip install streamlit==1.44.1 transformers Pillow==11.2.1
