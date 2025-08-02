import streamlit as st
from PIL import Image
import pytesseract
from ocr_utils import parse_questions
from qti_builder import build_qti_zip
import base64
import io

st.set_page_config(layout="wide")
st.title("💬 QuizMaker V1 – ChatGPT-Style Canvas Quiz Builder")

if "questions" not in st.session_state:
    st.session_state.questions = []

st.markdown("#### Paste or type a question below, or upload/paste a screenshot of a quiz question.")

with st.form("input_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        user_input = st.text_area("📝 Type or paste your question text here", height=150)
    with col2:
        uploaded_file = st.file_uploader("📎 Upload image", type=["png", "jpg", "jpeg"])
        base64_input = st.text_area("📋 Paste Base64 image (optional)", height=150)

    submitted = st.form_submit_button("➕ Add to Quiz")

    image = None
    if uploaded_file:
        image = Image.open(uploaded_file)
    elif base64_input:
        if "," in base64_input:
            base64_data = base64_input.split(",")[1]
        else:
            base64_data = base64_input
        try:
            img_bytes = base64.b64decode(base64_data)
            image = Image.open(io.BytesIO(img_bytes))
        except:
            st.error("Invalid base64 image")

    if submitted:
        if image:
            text = pytesseract.image_to_string(image)
            qlist = parse_questions(text)
            st.session_state.questions.extend(qlist)
        elif user_input:
            qlist = parse_questions(user_input)
            st.session_state.questions.extend(qlist)
        else:
            st.warning("Please provide either text or an image.")

st.markdown("---")
st.markdown("## 🧠 Preview: Canvas-Style Questions")

for i, q in enumerate(st.session_state.questions, 1):
    st.markdown(f"**Q{i}: {q['question']}**")
    for ident, ans in q['answers']:
        icon = "✅" if ident == q['correct'] else "◻️"
        st.markdown(f"- {icon} **{ident}.** {ans}")
    st.markdown("---")

if st.session_state.questions:
    if st.button("📥 Download QTI"):
        zip_path = build_qti_zip(st.session_state.questions, filename="full_quiz")
        with open(zip_path, "rb") as f:
            st.download_button("Download Canvas QTI", f, file_name="full_quiz.zip", mime="application/zip")
