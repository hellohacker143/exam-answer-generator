import streamlit as st
import google.generativeai as genai

# Configure API key for Google Generative AI
genai.configure(api_key="AIzaSyBZGHJwWL0_GnoimkOW52cDvqjRliCgeo0")

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(prompt):
    """Fetches a response from the Gemini Pro model."""
    try:
        response = chat.send_message(prompt, stream=True)
        return response
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return []

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo", layout="wide")

# CSS for styling
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #ff7e5f, #feb47b);
        color: #000000;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #434343, #000000);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.header("Gemini LLM Application")

# Initialize session state for categories
if 'categories' not in st.session_state:
    st.session_state['categories'] = {
        "Default": {'chat_history': [], 'old_responses': {}, 'name': "Default"}
    }
    st.session_state['current_category'] = "Default"
    st.session_state['selected_query'] = None

# Add a button to create a new chat
if st.sidebar.button("New Chat"):
    new_category = f"Chat {len(st.session_state['categories']) + 1}"
    st.session_state['categories'][new_category] = {
        'chat_history': [],
        'old_responses': {},
        'name': new_category
    }
    st.session_state['current_category'] = new_category
    st.success(f"Started a new chat session: '{new_category}'.")

# Sidebar for chat categories
with st.sidebar:
    st.title("Chat Categories")
    for category_key, category_data in st.session_state['categories'].items():
        if st.button(f"Switch to {category_data['name']}", key=f"switch_{category_key}"):
            st.session_state['current_category'] = category_key
            st.session_state['selected_query'] = None

    # Display the history for the selected category
    current_category = st.session_state['current_category']
    st.title(f"History: {st.session_state['categories'][current_category]['name']}")
    for query in st.session_state['categories'][current_category]['chat_history']:
        if st.button(query, key=f"history_{query}"):
            st.session_state['selected_query'] = query

# Get the current category
current_category = st.session_state['current_category']
category_data = st.session_state['categories'][current_category]

# Input field for user queries
user_input = st.text_input("Enter your query below:", key="user_query")
if st.button("Submit"):
    if user_input.strip():
        response = get_gemini_response(user_input)
        category_data['chat_history'].append(user_input)
        category_data['old_responses'][user_input] = response
        st.session_state['selected_query'] = user_input
    else:
        st.error("Please enter a query.")

# Display the selected query's response
if st.session_state['selected_query']:
    selected_query = st.session_state['selected_query']
    if selected_query in category_data['old_responses']:
        st.subheader("Response")
        st.write(f"**Query:** {selected_query}")
        for chunk in category_data['old_responses'][selected_query]:
            st.write(chunk.text)
