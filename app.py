import streamlit as st
import requests

# Gemini API setup
GEMINI_API_KEY = "AIzaSyCvzTcWX67xCTaFAQ9oSL1hI1Hwwe4DAwc"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

def generate_gemini_answer(topic, api_key):
    """Generate exam answer using Gemini API"""
    prompt = f"""Generate a perfect 15-marks university exam answer on the topic: "{topic}" in topper-writing style.
Follow this exact structure:

Introduction (4–5 bullet points)
Definition (4–5 bullet points)
Neat Diagram (text-based block diagram)
6 Key Points (Each with heading + 2–3 line explanation)
Features (4–5 bullet points)
Advantages (4–5 bullet points)
Characteristics (4–5 bullet points)
Applications / Real-world uses
Strong conclusion

Make the answer clean, structured, exam-oriented, and easy to score full marks.
Do NOT mention how many lines the sections should have. Generate the answer directly.
"""
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={api_key}",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error: API request failed with status code {response.status_code}. {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Exam Answer Generator", page_icon="📝", layout="wide")

st.title("📝 University Exam Answer Generator")
st.markdown("### Generate Perfect 15-Mark Exam Answers")
st.markdown("---")

# Input section
col1, col2 = st.columns([3, 1])

with col1:
    topic = st.text_input(
        "Enter your exam topic:",
        placeholder="e.g., Artificial Intelligence, Data Structures, Cloud Computing",
        help="Enter the topic for which you want to generate a 15-mark exam answer"
    )

with col2:
    st.write("")
    st.write("")
    generate_button = st.button("🚀 Generate Answer", use_container_width=True, type="primary")

st.markdown("---")

# Generate and display answer
if generate_button:
    if topic:
        with st.spinner("🔄 Generating your perfect exam answer... Please wait..."):
            answer = generate_gemini_answer(topic, GEMINI_API_KEY)
        
        if answer.startswith("Error:"):
            st.error(answer)
        else:
            st.success("✅ Answer generated successfully!")
            st.markdown("### 📄 Generated Answer:")
            st.markdown("---")
            
            # Display answer in a nice box
            st.markdown(
                f"""
                <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4;">
                {answer}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Download button
            st.download_button(
                label="📥 Download Answer as Text",
                data=answer,
                file_name=f"{topic.replace(' ', '_')}_exam_answer.txt",
                mime="text/plain"
            )
    else:
        st.warning("⚠️ Please enter a topic first!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666;">
        <p>Powered by <strong>Gemini API</strong> | Created with ❤️ using Streamlit</p>
        <p style="font-size: 0.8em;">Tip: Use specific topics for better results</p>
    </div>
    """,
    unsafe_allow_html=True
)
