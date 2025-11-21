import streamlit as st
import google.generativeai as genai
import bcrypt

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
st.set_page_config(page_title="Gemini LLM Application", layout="wide")

# CSS for default styling
st.markdown(
    """
    <style id="dynamic-style">
    body {
        background: #FFFFFF;
        color:rgb(102, 34, 34) 49, 49);
        font-family: "Courier New", Courier, monospace;
    }
    .sidebar .sidebar-content {
        background: #F5F5F5;
        color: #000000;
    }
    footer {
        background: #000000;
        color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# User management
if 'users' not in st.session_state:
    st.session_state['users'] = {}

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {}

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Authentication functions
def register_user(username, password):
    if username in st.session_state['users']:
        return False, "Username already exists."
    hashed_password = hash_password(password)
    st.session_state['users'][username] = hashed_password
    st.session_state['user_data'][username] = {
        "categories": {
            "Default": {'chat_history': [], 'old_responses': {}, 'name': "Default", 'saved_inputs': [], 'notes': ""}
        },
        "current_category": "Default",
        "selected_query": None,
        "page": "home"
    }
    return True, "Registration successful!"

def login_user(username, password):
    if username in st.session_state['users'] and check_password(password, st.session_state['users'][username]):
        st.session_state['authenticated'] = True
        st.session_state['current_user'] = username
        return True, "Login successful!"
    return False, "Invalid username or password."

def logout_user():
    st.session_state['authenticated'] = False
    st.session_state['current_user'] = None

# Control Panel for Admin to View Users
def control_panel():
    st.subheader("Control Panel: Registered Users")
    if st.session_state['users']:
        for username in st.session_state['users']:
            st.write(f"- {username}")
    else:
        st.write("No registered users.")

# Login/Signup UI
if not st.session_state['authenticated']:
    st.title("Welcome to  Augmented reality (AR) web page")

    auth_action = st.selectbox("Select Action", ["Login", "Sign Up", "Control Panel"], key="auth_action")

    if auth_action == "Control Panel":
        control_panel()
    else:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if auth_action == "Sign Up":
            if st.button("Register", key="register_btn"):
                success, message = register_user(username, password)
                if success:
                    st.success(message)
                else:
                    st.error(message)
        elif auth_action == "Login":
            if st.button("Login", key="login_btn"):
                success, message = login_user(username, password)
                if success:
                    st.success(message)
                else:
                    st.error(message)
else:
    current_user = st.session_state['current_user']
    user_data = st.session_state['user_data'][current_user]

    st.title(f"Gemini LLM Application - Welcome {current_user}")
    st.write("Explore the power of AI with categorized chats and insights.")

    if st.button("Logout"):
        logout_user()
        st.success("You have been logged out.")

    # Application logic
    if 'categories' not in user_data:
        user_data['categories'] = {
            "Default": {'chat_history': [], 'old_responses': {}, 'name': "Default", 'saved_inputs': [], 'notes': ""}
        }
        user_data['current_category'] = "Default"
        user_data['selected_query'] = None

    # Sidebar for categories
    st.sidebar.title("Chat Folders")
    for category_key, category_data in user_data['categories'].items():
        if st.sidebar.button(category_data['name'], key=f"sidebar_category_{category_key}"):
            user_data['current_category'] = category_key
            user_data['page'] = 'categories'

    # Add New Chat Button
    if st.sidebar.button("New Chat"):
        new_chat_name = f"Chat {len(user_data['categories']) + 1}"
        user_data['categories'][new_chat_name] = {'chat_history': [], 'old_responses': {}, 'name': new_chat_name, 'saved_inputs': [], 'notes': ""}
        user_data['current_category'] = new_chat_name
        user_data['page'] = 'categories'

    # Home Page Navigation
    if 'page' not in user_data:
        user_data['page'] = 'home'

    if user_data['page'] == 'home':
        st.subheader("Chat Categories")
        for category_key, category_data in user_data['categories'].items():
            if st.button(category_data['name'], key=f"category_home_{category_key}"):
                user_data['current_category'] = category_key
                user_data['page'] = 'categories'

    elif user_data['page'] == 'categories':
        current_category = user_data['current_category']
        category_data = user_data['categories'][current_category]

        st.subheader(f"Chat Category: {category_data['name']}")

        # Rename category inline
        new_name = st.text_input("Rename Category:", value=category_data['name'], key=f"rename_{current_category}")
        if new_name and new_name != category_data['name']:
            category_data['name'] = new_name

        # History Section
        st.markdown('<div class="history-section">', unsafe_allow_html=True)
        if category_data['chat_history']:
            st.markdown('<div class="history-grid">', unsafe_allow_html=True)
            for i, query in enumerate(category_data['chat_history']):
                if st.button(query, key=f"history_{current_user}_{current_category}_{i}"):
                    user_data['selected_query'] = query
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.write("No history yet.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Input field for user queries
        user_input = st.text_input("Enter your query below:", key="user_query")
        if st.button("Submit"):
            if user_input.strip():
                response = get_gemini_response(user_input)
                category_data['chat_history'].append(user_input)
                category_data['old_responses'][user_input] = response
                user_data['selected_query'] = user_input
            else:
                st.error("Please enter a query.")

        # Response Section
        if user_data['selected_query']:
            selected_query = user_data['selected_query']
            if selected_query in category_data['old_responses']:
                st.subheader("Response")
                st.write(f"**Query:** {selected_query}")
                response = category_data['old_responses'][selected_query]
                if response:
                    for chunk in response:
                        if hasattr(chunk, "text"):
                            st.write(chunk.text)
                        else:
                            st.warning(f"Incomplete response. Finish reason: {chunk.finish_reason}")
                else:
                    st.error("No response received.")

        # Add Text Area for Notes
        st.markdown('<div class="textarea-container">', unsafe_allow_html=True)
        note = st.text_area("Notes:", value=category_data.get('notes', ""), key=f"notes_{current_category}")
        category_data['notes'] = note
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Go Back to Home"):
            user_data['page'] = 'home'
