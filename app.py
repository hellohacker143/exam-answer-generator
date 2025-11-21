import streamlit as st
import google.generativeai as genai

# Configure your Google Generative AI API key here
genai.configure(api_key="AIzaSyAkEHc1wTyuxUVAO2Is9fqLQS9EuSae8TI")
model = genai.GenerativeModel("gemini-1.5-flash")


# Function to get AI response from Google Generative AI
def get_ai_response(user_input):
    try:
        response = model.generate_content(user_input)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("Google Generative AI Response")

# Input box for user
user_input = st.text_input("Enter your question or input:", "")

if user_input:
    # Generate response if user input is not empty
    response = get_ai_response(user_input)
    st.write("**Response:**", response)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<footer style='text-align:center;'>Made with Streamlit | Powered by Google Generative AI</footer>", unsafe_allow_html=True)
