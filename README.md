# 🎬 AI Video Assistant

An intelligent AI-powered Video Assistant that transforms YouTube videos and local media files into actionable insights. Upload a video or provide a YouTube link to generate transcripts, summaries, action items, key decisions, and interact with your content using a conversational AI chatbot.

## 🚀 Features

### 🎥 Video & Audio Processing

* Supports YouTube URLs
* Supports local video and audio files
* Automatic audio extraction

### ✍️ AI Transcription

* Whisper-powered speech-to-text
* Multi-language support
* Accurate transcript generation

### 📋 Smart Summarization

* AI-generated video summaries
* Automatic title generation
* Key takeaways extraction

### ✅ Action Item Extraction

* Detects tasks and responsibilities
* Generates actionable insights
* Highlights important follow-ups

### 🔑 Key Decision Detection

* Identifies important decisions discussed
* Organizes decision points clearly

### ❓ Open Question Detection

* Extracts unanswered questions
* Helps track pending discussions

### 🤖 Chat With Your Video

* RAG-powered conversational AI
* Ask questions about video content
* Context-aware responses
* Semantic search capabilities

### 🎨 Modern UI

* Beautiful Streamlit interface
* Interactive progress tracking
* Dark-themed professional dashboard
* Responsive design

---

## 🏗️ Project Structure

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
├── utils/
│   └── audio_processor.py
│
├── App.py
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Tech Stack

### Frontend

* Streamlit
* HTML/CSS
* Custom UI Components

### Backend

* Python
* LangChain
* ChromaDB

### AI Models

* OpenAI GPT Models
* Whisper Speech Recognition
* Sentence Transformers
* Embedding Models

### Vector Database

* ChromaDB
* Semantic Search

---

## 📦 Installation

### Clone Repository

```bash
git clone https://github.com/MONJIT07/Video-Agent.git
cd Video-Agent
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

Add any additional API keys required by your implementation.

---

## ▶️ Run Application

```bash
streamlit run App.py
```

Open:

```text
http://localhost:8501
```

---

## 🧠 How It Works

1. User submits a YouTube URL or local file.
2. Audio is extracted and processed.
3. Whisper generates transcripts.
4. AI creates summaries and titles.
5. Action items, decisions, and questions are extracted.
6. Transcript is indexed into a vector database.
7. Users interact with content through a RAG-powered chatbot.

---

## 📸 Screenshots

Add screenshots of:

* Home Page
* Processing Pipeline
* Summary Dashboard
* Chat Interface

Example:

```markdown
![Dashboard](images/dashboard.png)
```

---

## 🎯 Future Improvements

* Speaker diarization
* Real-time transcription
* PDF export
* Meeting analytics
* Multi-video knowledge base
* Team collaboration features
* Cloud deployment support

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Monjit Tamuli**

Electrical Engineering Student | NIT Silchar

Passionate about AI, Machine Learning, Cloud Computing, and Software Development.
