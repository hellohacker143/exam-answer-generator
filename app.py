import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyAkEHc1wTyuxUVAO2Is9faLQS9Eu5ae8TI")
model = genai.GenerativeModel("gemini-1.5-flash")

# Page config
st.set_page_config(page_title="Exam Answer Generator", page_icon="📝")

# Title
st.title("📝 Exam Answer Generator")
st.write("Generate perfect 15-mark university exam answers")

# Input
topic = st.text_input("Enter your exam topic:", placeholder="e.g., Artificial Intelligence")

# Generate button
if st.button("🚀 Generate Answer"):
    if topic:
        with st.spinner("Generating your answer..."):
            # Create prompt
            prompt = f"""Generate a perfect 15-mark university exam answer on: {topic}

Structure:
1. Introduction (4-5 points)
2. Definition (4-5 points)
3. Diagram (text-based)
4. 6 Key Points (with explanations)
5. Features (4-5 points)
6. Advantages (4-5 points)
7. Characteristics (4-5 points)
8. Applications
9. Conclusion

Make it exam-ready and well-structured."""

            try:
                # Get response from Gemini
                response = model.generate_content(prompt)
                
                # Display answer
                st.success("✅ Answer generated!")
                st.markdown("### Your Answer:")
                st.write(response.text)
                
                # Download button
                st.download_button(
                    label="📥 Download Answer",
                    data=response.text,
                    file_name=f"{topic}_answer.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a topic!")

# Footer
st.markdown("---")
st.caption("Powered by Google Gemini AI")
