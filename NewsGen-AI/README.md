# NewsGen AI 📰

### AI-Powered Daily News Intelligence & Summarization Platform

NewsGen AI is an intelligent news aggregation and summarization platform that collects news articles from multiple RSS feeds, removes duplicate articles, and generates concise, meaningful summaries using Large Language Models (LLMs).

The application provides a centralized dashboard where users can explore the latest news, discover important stories, and consume information through AI-generated summaries.

Built using **Python, FastAPI, React, LangChain, Ollama, Llama 3.2, and SQLite**, NewsGen AI aims to simplify daily news consumption through AI-powered automation.

---

## 🚀 Project Overview

In today's digital world, information is available across hundreds of news websites and platforms. Keeping up with important developments can be time-consuming.

NewsGen AI addresses this challenge by automating the news collection and summarization process.

The platform follows an AI-powered workflow:

1. Fetch news articles from configured RSS feeds.
2. Extract article titles, descriptions, publication dates, and source information.
3. Clean article content and remove duplicate news.
4. Process selected articles using an LLM.
5. Generate concise and readable AI summaries.
6. Store news information and summaries in SQLite.
7. Display the processed news through an interactive React dashboard.

**Project Goal:** Build a lightweight, locally executable AI news intelligence platform with automated summarization and scheduled news delivery.

---

## ✨ Key Features

### 1. Automated News Aggregation
- Fetch news from multiple RSS sources.
- Extract article metadata.
- Handle RSS feed errors and network failures.
- Support multiple news categories.

### 2. AI-Powered Summarization
- Generate concise news summaries using Llama 3.2.
- Run LLM inference locally using Ollama.
- Reduce lengthy news content into readable summaries.
- Configure summarization prompts for consistent output.

### 3. Duplicate News Detection
- Identify duplicate articles.
- Reduce repeated news entries.
- Maintain a cleaner news collection.

### 4. Interactive News Dashboard
- Modern React-based user interface.
- Explore articles by category.
- View article details.
- Display AI-generated summaries.
- Access original news sources.

### 5. Database Management
- Store fetched news articles.
- Maintain article metadata.
- Store processed information using SQLite.

### 6. Scheduling and News Delivery
- Planned capability for automated daily news processing.
- Configurable execution schedules.
- Planned email-based daily news digest delivery.

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Frontend | React.js |
| Backend Framework | FastAPI |
| AI Framework | LangChain |
| Large Language Model | Llama 3.2 |
| Local LLM Runtime | Ollama |
| News Collection | RSS Feeds |
| Database | SQLite |
| Frontend Build Tool | Vite |
| API Communication | REST APIs |
| Version Control | Git & GitHub |

---

## 🏗️ System Architecture

```text
                  NEWSGEN AI
                      |
                      v
              RSS NEWS SOURCES
                      |
                      v
              NEWS FETCHING ENGINE
                 (Python)
                      |
                      v
               CONTENT CLEANING
                      |
                      v
              DUPLICATE DETECTION
                      |
                      v
               ARTICLE PROCESSING
                      |
                      v
               LANGCHAIN PIPELINE
                      |
                      v
                OLLAMA ENGINE
                      |
                      v
                 LLAMA 3.2
                      |
                      v
              AI SUMMARIZATION
                      |
                      v
                SQLITE DATABASE
                      |
                      v
               FASTAPI BACKEND
                      |
                      v
               REACT FRONTEND
                      |
                      v
               NEWSGEN DASHBOARD
```

---

## 📂 Project Structure

```text
NewsGen-AI/
│
├── backend/
│   │
│   ├── app/
│   │   ├── main.py
│   │   ├── news_fetcher.py
│   │   ├── summarizer.py
│   │   ├── database.py
│   │   ├── Create database.py
│   │   ├── check_database.py
│   │   ├── run_database_pipeline.py
│   │   ├── run_news_summarizer.py
│   │   └── test_ollama.py
│   │
│   ├── data/
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## ⚙️ How It Works

### Step 1: News Collection

The news fetching engine connects to configured RSS feeds and retrieves available articles.

The extracted information includes:

- Article title
- Article description
- Article URL
- Publication date
- News source

### Step 2: Content Cleaning

Raw RSS descriptions may contain HTML tags and unnecessary whitespace.

The application cleans the extracted content before further processing.

### Step 3: Duplicate Detection

The deduplication process identifies repeated articles and filters them before summarization.

### Step 4: AI Summarization

The selected articles are passed to the local LLM through Ollama.

Llama 3.2 generates concise summaries using the configured prompts.

### Step 5: Database Storage

Article information and processed results are managed using SQLite.

### Step 6: Frontend Presentation

The React dashboard communicates with the FastAPI backend to display the collected news and available AI summaries.

---

## 💻 Installation and Setup

### Prerequisites

Install the following:

- Python 3.10 or later
- Node.js and npm
- Git
- Ollama

### 1. Clone the Repository

```bash
git clone https://github.com/mouneshvaddi/Ai_Projects.git
```

Navigate to the project:

```bash
cd Ai_Projects/NewsGen-AI
```

### 2. Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

### 3. Ollama Setup

Download and install Ollama from:

https://ollama.com/

Download the Llama 3.2 model:

```bash
ollama pull llama3.2
```

Run the model:

```bash
ollama run llama3.2
```

Ollama provides a local inference environment for running the language model.

### 4. Start FastAPI Backend

From the backend directory:

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the URL provided by Vite, usually:

```text
http://localhost:5173
```

---

## 🔐 Environment Configuration

Create a `.env` file in the backend directory if required by your configuration.

Configure the necessary application settings, such as:

- Ollama model name
- Ollama API URL
- RSS feed configuration
- Database path
- Backend configuration

Never commit API keys, credentials, passwords, or private environment variables to GitHub.

---

## 📊 Future Enhancements

The following features are planned for future development:

- Automated daily news scheduling.
- Personalized news preferences.
- Email-based daily news delivery.
- News sentiment analysis.
- Topic-based news recommendations.
- Advanced news analytics dashboard.
- Article importance ranking.
- Support for additional local and cloud LLMs.
- Public cloud deployment.

---

## 🔮 Project Vision

NewsGen AI aims to transform traditional news consumption into an intelligent, personalized, and automated experience.

By combining news aggregation, local LLM inference, and modern web technologies, the platform provides a foundation for building an AI-powered news intelligence system.

---

## 👨‍💻 Author

**Mounesh Vaddi**

Python Developer | Generative AI | LLM Applications | Automation

GitHub: https://github.com/mouneshvaddi

---

## 📄 License

This project is available for learning, experimentation, and development. A formal open-source license can be added when selected.
