
import os
import uuid
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions
)
from core.rag_engine import build_rag_chain, ask_question


# ----------------------------------
# Configuration
# ----------------------------------

load_dotenv()

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎥",
    layout="wide"
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ----------------------------------
# Backend Pipeline
# ----------------------------------

def run_pipeline(source: str, language: str = "english") -> dict:

    chunks = process_input(source)

    transcript = transcribe_all(chunks, language)

    if not transcript or not transcript.strip():
        raise ValueError("No transcription was generated.")

    title = generate_title(transcript)

    summary = summarize(transcript)

    action_items = extract_action_items(transcript)

    decisions = extract_key_decisions(transcript)

    questions = extract_questions(transcript)

    rag_chain = build_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain
    }


# ----------------------------------
# Session State
# ----------------------------------

if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ----------------------------------
# Application Header
# ----------------------------------

st.title("🎥 AI Video Assistant")

st.markdown(
    """
    ### Your intelligent video and meeting companion

    Upload a video or audio file, or paste a YouTube URL.

    Automatically generate transcripts, summaries, action items,
    key decisions and chat with your content.
    """
)

st.divider()


# ----------------------------------
# Input Section
# ----------------------------------

st.subheader("1. Upload Your Content")

input_method = st.radio(
    "Choose your input method:",
    ["YouTube URL", "Upload Video / Audio"],
    horizontal=True
)

source = None

if input_method == "YouTube URL":

    youtube_url = st.text_input(
        "Enter YouTube URL",
        placeholder="https://www.youtube.com/watch?v=..."
    )

    if youtube_url.strip():
        source = youtube_url.strip()

else:

    uploaded_file = st.file_uploader(
        "Upload your video or audio file",
        type=["mp4", "mp3", "wav", "m4a", "webm", "mov", "mkv"]
    )

    if uploaded_file is not None:

        st.success(f"Uploaded: {uploaded_file.name}")

        if st.button("Prepare Uploaded File"):
            extension = Path(uploaded_file.name).suffix

            unique_name = f"{uuid.uuid4().hex}{extension}"

            file_path = os.path.join(
                UPLOAD_DIR,
                unique_name
            )

            with open(file_path, "wb") as file:
                file.write(uploaded_file.getbuffer())

            st.session_state.upload_path = file_path

        source = st.session_state.get("upload_path")


# ----------------------------------
# Language Selection
# ----------------------------------

language = st.selectbox(
    "Select transcription language",
    ["english", "hinglish"]
)


# ----------------------------------
# Process Button
# ----------------------------------

if st.button(
    "Generate AI Analysis",
    type="primary",
    use_container_width=True
):

    if not source:

        st.warning("Please provide a YouTube URL or upload a file.")

    else:

        try:

            with st.spinner(
                "Processing your video... This may take some time."
            ):

                result = run_pipeline(source, language)

                st.session_state.result = result

                # Reset previous conversation
                st.session_state.chat_history = []

            st.success("Your AI analysis is ready!")

        except Exception as e:

            st.error(f"Something went wrong: {str(e)}")


# ----------------------------------
# Display Results
# ----------------------------------

if st.session_state.result is not None:

    result = st.session_state.result

    st.divider()

    st.header("2. AI Generated Analysis")

    st.title(result["title"])

    # Tabs for different results

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Summary",
            "Action Items",
            "Key Decisions",
            "Open Questions",
            "Transcript"
        ]
    )

    with tab1:

        st.subheader("Meeting Summary")

        st.write(result["summary"])

    with tab2:

        st.subheader("Action Items")

        st.write(result["action_items"])

    with tab3:

        st.subheader("Key Decisions")

        st.write(result["key_decisions"])

    with tab4:

        st.subheader("Open Questions")

        st.write(result["open_questions"])

    with tab5:

        st.subheader("Full Transcript")

        st.text_area(
            "Transcript",
            value=result["transcript"],
            height=400
        )

    # ----------------------------------
    # Download Section
    # ----------------------------------

    st.divider()

    st.subheader("3. Download Your Results")

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="Download Transcript",
            data=result["transcript"],
            file_name="transcript.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:

        report = f"""
TITLE:
{result['title']}

SUMMARY:
{result['summary']}

ACTION ITEMS:
{result['action_items']}

KEY DECISIONS:
{result['key_decisions']}

OPEN QUESTIONS:
{result['open_questions']}
"""

        st.download_button(
            label="Download AI Report",
            data=report,
            file_name="meeting_report.txt",
            mime="text/plain",
            use_container_width=True
        )

    # ----------------------------------
    # RAG Chat Section
    # ----------------------------------

    st.divider()

    st.header("4. Chat With Your Video")

    st.write(
        "Ask questions about your uploaded video or meeting."
    )

    rag_chain = result["rag_chain"]

    # Display previous conversation

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.write(message["content"])

    # Chat input

    user_question = st.chat_input(
        "Ask something about your video..."
    )

    if user_question:

        # Display user message

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        with st.chat_message("user"):
            st.write(user_question)

        # Generate AI response

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    answer = ask_question(
                        rag_chain,
                        user_question
                    )

                    st.write(answer)

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                except Exception as e:

                    st.error(f"Chat error: {str(e)}")


# ----------------------------------
# Footer
# ----------------------------------

st.divider()

st.caption(
    "AI Video Assistant | Built with Python, Streamlit, "
    "LangChain and RAG"
)
