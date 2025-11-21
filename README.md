# 📝 Exam Answer Generator

AI-powered Streamlit app that generates perfect 15-mark university exam answers using Google Gemini API in topper-writing style.

## ✨ Features

- 🤖 **AI-Powered Generation**: Uses Google Gemini Pro AI model
- 📚 **Structured Answers**: Follows university exam answer format
- 🎯 **15-Marks Format**: Specifically designed for 15-mark questions
- 💾 **Download Option**: Save generated answers as text files
- 🎨 **Modern UI**: Beautiful and user-friendly interface
- ⚡ **Fast Generation**: Quick response times

## 🚀 Live Demo

[Try it on Streamlit Cloud](#) _(Deploy to add link)_

## 📋 Answer Structure

The app generates answers with the following structure:
1. **Introduction** (4–5 bullet points)
2. **Definition** (4–5 bullet points)
3. **Neat Diagram** (text-based block diagram)
4. **6 Key Points** (Each with heading + 2–3 line explanation)
5. **Features** (4–5 bullet points)
6. **Advantages** (4–5 bullet points)
7. **Characteristics** (4–5 bullet points)
8. **Applications** / Real-world uses
9. **Strong conclusion**

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/hellohacker143/exam-answer-generator.git
cd exam-answer-generator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API Key**
   
   Open `app.py` and replace the API_KEY with your Google Gemini API key:
   ```python
   API_KEY = "your-gemini-api-key-here"
   ```

4. **Run the app**
```bash
streamlit run app.py
```

## 🔑 Getting Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

## 📦 Dependencies

- `streamlit>=1.28.0` - Web framework
- `google-generativeai>=0.3.0` - Gemini AI integration

## 💻 Usage

1. Open the app in your browser (usually http://localhost:8501)
2. Enter your exam topic in the text input field
3. Click "🚀 Generate Answer (Send)"
4. Wait for the AI to generate your answer
5. Download the answer using the download button (optional)

## 📸 Screenshots

_Add screenshots of your app here_

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**hellohacker143**
- GitHub: [@hellohacker143](https://github.com/hellohacker143)

## ⭐ Show your support

Give a ⭐ if this project helped you!

## 🙏 Acknowledgments

- Google Gemini AI for powering the answer generation
- Streamlit for the amazing web framework
- All contributors and users

---

**Note**: This tool is for educational purposes. Always verify and customize generated answers according to your needs.
