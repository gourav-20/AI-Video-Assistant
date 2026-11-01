# AI Video Assistant

An AI-powered application that converts video and audio content into meaningful information using speech recognition and Generative AI. It helps users understand long videos and meetings through transcription, summarization, action-item extraction, and AI-powered question answering.

## Features

- **Multiple Input Sources:** Process YouTube videos and locally uploaded audio/video files.
- **Audio Extraction:** Extract audio from video files using FFmpeg.
- **Audio Chunking:** Divide long audio files into smaller chunks for processing.
- **English Transcription:** Generate transcripts using OpenAI Whisper.
- **Hinglish Transcription:** Use Sarvam AI to transcribe Hinglish speech and translate it into English.
- **AI Summarization:** Generate concise summaries using an LLM.
- **Action Item Extraction:** Identify tasks, responsible owners, and deadlines from transcripts.
- **Key Decision Extraction:** Identify important decisions discussed in meetings.
- **Open Question Extraction:** Find unresolved questions and follow-up topics.
- **RAG-Based Chatbot:** Ask questions about the processed video or meeting transcript.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | User interface |
| OpenAI Whisper | Speech-to-text transcription |
| Sarvam AI | Hinglish speech transcription and translation |
| Groq API | LLM inference |
| LangChain | LLM application development |
| ChromaDB | Vector database |
| HuggingFace | Text embeddings |
| FFmpeg | Audio extraction and conversion |
| Pydub | Audio processing and chunking |

## Project Architecture

```text
AI-Video-Assistant/
│
├── core/
│   ├── transcriber.py
│   ├── summarize.py
│   ├── extractor.py
│   └── rag_engine.py
│
├── utils/
│   └── audio_processor.py
│
├── downloads/
├── uploads/
├── vector_db/
│
├── app.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

*Note: The folders above describe the intended project organization. Your actual repository may contain additional files.*

## How It Works

1. The user provides a YouTube URL or uploads a local audio/video file.
2. FFmpeg extracts audio from the input.
3. The audio is divided into smaller chunks.
4. Whisper or Sarvam AI processes the audio and generates a transcript.
5. The transcript is sent to the LLM for summarization and information extraction.
6. Important action items, key decisions, and open questions are generated.
7. The transcript is processed into embeddings and stored in ChromaDB.
8. The RAG chatbot retrieves relevant transcript information to answer user questions.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/gourav-20/AI-Video-Assistant.git
```

Navigate to the project directory:

```bash
cd AI-Video-Assistant
```

### 2. Create a Virtual Environment

Using uv:

```bash
uv venv
```

Activate it in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
uv pip install -r requirements.txt
```

### 4. Install FFmpeg

Install FFmpeg on your system and configure its `bin` directory in the system PATH.

Verify installation:

```bash
ffmpeg -version
```

### 5. Configure Environment Variables

Create a `.env` file in the project root.

Add your API credentials:

```env
GROQ_API_KEY=your_groq_api_key
SARVAM_API_KEY=your_sarvam_api_key

WHISPER_MODEL=small
SARVAM_STT_MODEL=saaras:v2.5
```

Replace the placeholder values with your actual API keys.

**Important:** Never upload your `.env` file or expose your API keys on GitHub.

### 6. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the application.

## Environment Requirements

- Python 3.10 or newer (use a version compatible with the installed dependencies).
- FFmpeg installed and configured in PATH.
- Groq API key.
- Sarvam AI API key for Hinglish transcription.
- Internet connection for API-based processing and YouTube downloads.

## Future Improvements

- Improve transcription accuracy for multilingual audio.
- Add speaker identification.
- Improve RAG retrieval accuracy and relevance filtering.
- Add PDF and TXT export options.
- Add Docker support.
- Deploy the application online.

## Author

**Gourav Tambulkar**

Python Developer | Generative AI Enthusiast

GitHub: [gourav-20](https://github.com/gourav-20)