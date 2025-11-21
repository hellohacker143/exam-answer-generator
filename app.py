import streamlit as st
import google.generativeai as genai

# Configure Gemini API
API_KEY = "AIzaSyCvzTcWX67xCTaFAQ9oSL1hI1Hwwe4DAwc"
genai.configure(api_key=API_KEY)

# Default 15-marks university answer prompt
DEFAULT_PROMPT = """
Generate a perfect 15-marks university exam answer on the topic: "{topic}" in topper-writing style.

Follow this exact structure:
1. Introduction (4–5 bullet points)
2. Definition (4–5 bullet points)
3. Neat Diagram (text-based block diagram)
4. 6 Key Points (Each with heading + 2–3 line explanation)
5. Features (4–5 bullet points)
6. Advantages (4–5 bullet points)
7. Characteristics (4–5 bullet points)
8. Applications / Real-world uses
9. Strong conclusion

Make the answer clean, structured, exam-oriented, and easy to score full marks.
Do NOT mention how many lines the sections should have. Generate the answer directly.
"""

def generate_answer(topic):
    """Generate exam answer using Gemini API"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = DEFAULT_PROMPT.format(topic=topic)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating answer: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Exam Answer Generator", page_icon="📝", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 30px;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 12px 30px;
        border-radius: 8px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #155a8a;
    }
    .answer-box {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📝 University Exam Answer Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Generate perfect 15-marks answers in topper-writing style</div>', unsafe_allow_html=True)

# Input section
topic = st.text_input(
    "Enter your topic:",
    placeholder="e.g., Artificial Intelligence, Data Structures, Cloud Computing...",
    help="Enter any university exam topic"
)

# Generate button
if st.button("🚀 Generate Answer (Send)"):
    if topic:
        with st.spinner("✨ Generating your perfect exam answer..."):
            answer = generate_answer(topic)
            
            st.success("✅ Answer generated successfully!")
            
            # Display answer in a nice box
            st.markdown('<div class="answer-box">', unsafe_allow_html=True)
            st.markdown("### 📄 Generated Answer:")
            st.markdown(answer)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Download button
            st.download_button(
                label="📥 Download Answer",
                data=answer,
                file_name=f"{topic.replace(' ', '_')}_answer.txt",
                mime="text/plain"
            )
    else:
        st.warning("⚠️ Please enter a topic first!")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #888;">'
    'Powered by Google Gemini AI | Made with ❤️ using Streamlit'
    '</div>',
    unsafe_allow_html=True
)
