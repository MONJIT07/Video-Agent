# 🎬 AI Video Assistant

AI Video Assistant is an intelligent video analysis platform that converts YouTube videos and local media files into searchable knowledge.

The application automatically transcribes audio, generates summaries, extracts action items, identifies key decisions, and allows users to chat with their video content using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

### 🎥 Video Processing

* Analyze YouTube videos
* Analyze local video/audio files
* Automatic audio extraction

### 🎙 Speech-to-Text

* Whisper-powered transcription
* Multi-language support
* High-quality speech recognition

### 📝 AI Summarization

* Mistral AI powered summaries
* Automatic title generation
* Key insights extraction

### ✅ Action Item Detection

* Extract tasks and responsibilities
* Identify follow-up actions
* Meeting and lecture analysis

### 🔑 Key Decision Extraction

* Detect important decisions
* Organize discussion outcomes

### ❓ Question Extraction

* Identify open questions
* Track unresolved discussion points

### 🤖 Chat With Your Video

* RAG-powered conversational interface
* Context-aware responses
* Semantic search over transcripts

### 🎨 Modern Streamlit UI

* Interactive dashboard
* Animated processing pipeline
* Dark theme professional interface

---

## 🏗 Architecture

```text
User Input
     │
     ▼
Video / Audio Processing
     │
     ▼
Whisper Transcription
     │
     ▼
Mistral AI Summarization
     │
     ▼
Information Extraction
(Action Items • Decisions • Questions)
     │
     ▼
ChromaDB Vector Storage
     │
     ▼
RAG Chat Interface
```

---

## 🛠 Tech Stack

### Frontend

* Streamlit
* HTML
* CSS

### AI & NLP

* Mistral AI
* Sarvam AI
* Whisper
* Sentence Transformers

### Vector Database

* ChromaDB

### Backend

* Python

---

## 📂 Project Structure

```text
video-agent/
│
├── core/
│   ├── extractor.py
│   ├── rage.py
│   ├── summarizer.py
│   ├── transcriber.py
│   └── vectorStore.py
│
├── downloads/
├── vector_db/
│
├── App.py
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙ Environment Variables

Create a `.env` file:

```env
MISTRAL_API_KEY=your_mistral_api_key

SARVAM_API_KEY=your_sarvam_api_key
SARVAM_STT_MODEL=sarvam-small

WHISPER_MODEL=small
```

Never upload your `.env` file to GitHub.

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/MONJIT07/Video-Agent.git
cd Video-Agent
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶ Run Application

```bash
streamlit run App.py
```

Open:

```text
http://localhost:8501
```

---

## 🔄 Workflow

1. Provide a YouTube URL or local media file.
2. Audio is extracted.
3. Whisper generates transcripts.
4. Mistral AI creates summaries.
5. Action items, decisions, and questions are extracted.
6. Transcript embeddings are stored in ChromaDB.
7. Users interact with content through the AI chatbot.

---

## 🌟 Use Cases

* Meeting Analysis
* Lecture Summarization
* Podcast Insights
* Educational Content Review
* Interview Analysis
* Research Video Understanding

---

## 📈 Future Enhancements

* Speaker Diarization
* Real-Time Transcription
* PDF Report Export
* Multi-Video Knowledge Base
* Cloud Deployment
* Team Collaboration Features

---

## 👨‍💻 Author

**Monjit Tamuli**

Electrical Engineering Student
National Institute of Technology Silchar

Interested in Artificial Intelligence, Machine Learning, Cloud Computing, and Software Development.

---

## 📜 License

This project is licensed under the MIT License.
