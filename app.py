import streamlit as st
import google.generativeai as genai

# ------------------------------------------------
# 🔐 Load API key safely from Streamlit secrets
# ------------------------------------------------
genai.configure(api_key=st.secrets["AIzaSyCvzTcWX67xCTaFAQ9oSL1hI1Hwwe4DAwc"])

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


# ------------------------------------------------
# 🔥 Function: Stream Gemini Response
# ------------------------------------------------
def get_gemini_response(prompt):
    try:
        response_stream = chat.send_message(prompt, stream=True)
        return response_stream
    except Exception as e:
        st.error(f"Error: {e}")
        return []


# ------------------------------------------------
# 🎨 Streamlit UI Setup
# ------------------------------------------------
st.set_page_config(page_title="Gemini Multi-Chat App", layout="wide")

# Background CSS
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #ff7e5f, #feb47b);
        color: #000;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #202020, #000000);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.header("🔥 Gemini Pro — Multi Chat Application")


# ------------------------------------------------
# 🌐 Initialize Session State
# ------------------------------------------------
if "categories" not in st.session_state:
    st.session_state["categories"] = {
        "Default": {"chat_history": [], "responses": {}}
    }
    st.session_state["current_category"] = "Default"
    st.session_state["selected_query"] = None


# ------------------------------------------------
# 🧭 Sidebar: Chat Management
# ------------------------------------------------
with st.sidebar:
    st.title("Chats")

    # ➕ Create New Chat
    if st.button("➕ New Chat"):
        new_name = f"Chat {len(st.session_state['categories']) + 1}"
        st.session_state["categories"][new_name] = {
            "chat_history": [],
            "responses": {},
        }
        st.session_state["current_category"] = new_name
        st.success(f"Created: {new_name}")

    # 🔄 Switch Between Chats
    for key in st.session_state["categories"]:
        if st.button(f"Switch: {key}", key=f"switch_{key}"):
            st.session_state["current_category"] = key
            st.session_state["selected_query"] = None

    # 🕘 Display History
    st.title("History")
    cat = st.session_state["current_category"]
    for q in st.session_state["categories"][cat]["chat_history"]:
        if st.button(q, key=f"his_{q}"):
            st.session_state["selected_query"] = q


# ------------------------------------------------
# 📝 Main Input
# ------------------------------------------------
user_input = st.text_input("Ask your question:")

if st.button("Submit"):
    if user_input.strip():
        current = st.session_state["current_category"]

        # Save the question
        st.session_state["categories"][current]["chat_history"].append(user_input)

        # Stream response
        stream = get_gemini_response(user_input)
        st.session_state["categories"][current]["responses"][user_input] = stream

        # Show this query immediately
        st.session_state["selected_query"] = user_input
    else:
        st.error("Please enter something before submitting!")


# ------------------------------------------------
# 📩 Display Streaming Response
# ------------------------------------------------
if st.session_state["selected_query"]:
    query = st.session_state["selected_query"]
    cat = st.session_state["current_category"]

    st.subheader("Response")
    st.write(f"**You asked:** {query}")

    response_stream = st.session_state["categories"][cat]["responses"][query]

    output = ""
    placeholder = st.empty()

    for chunk in response_stream:
        output += chunk.text
        placeholder.markdown(output)
