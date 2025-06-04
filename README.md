# 📰 AI News Aggregator & Chatbot

A full-stack AI-powered system that scrapes Australian news, summarizes daily highlights, and answers user questions using RAG (Retrieval-Augmented Generation).

---

## ⚙️ Tech Stack

- **Backend:** FastAPI, HuggingFace Transformers, FAISS
- **Frontend:** React + Axios
- **Scraper:** Requests + BeautifulSoup
- **DevOps:** Docker, Docker Compose

---

## ✅ Features

- 🔎 Scrapes news from ABC, The Guardian, and The New Daily
- 🧠 Summarizes and highlights news by category (sports, finance, lifestyle, music)
- 🔁 Detects duplicates using cosine similarity + clustering
- 🌟 Flags priority articles using keywords (e.g., "breaking", "exclusive")
- 💬 Chatbot uses semantic search (FAISS) + text generation (RAG)
- 📊 Clean React UI to display highlights by category

---

## 🧪 Pipeline Overview

### 1. `summarize.py`
- Model: `t5-small` or `declare-lab/flan-alpaca-base`
- Summarizes raw article text
- Saves to: `combined_articles_with_summary.json`

### 2. `create_highlights.py`
- Embedding Model: `all-MiniLM-L6-v2`
- Detects duplicate stories via cosine similarity
- Flags articles with breaking news keywords
- Output: `combined_articles_with_summary_highlights.json`

### 3. `create_faiss_index.py`
- Uses SentenceTransformer for embedding highlights
- Stores searchable index in FAISS: `highlight_index.faiss`
- Metadata stored in: `metadata.json`

---

## 🚀 Quick Start (Docker)

### Step 1: Clean existing containers (if any)
```bash
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q) --force
```

### Step 2: Build and start containers
```bash
docker-compose up --build
```

### Step 3: Run the pipeline (ONLY FIRST TIME)
```bash
docker exec -it news-backend bash
python pipeline.py
```

> ⚠️ The backend won't start correctly until the pipeline is run once and necessary JSON/FAISS files are created.

---

## 🔗 API Endpoints

- `GET /api/highlights` → Returns list of categorized news highlights
- `POST /api/ask` → Accepts user question and returns RAG-generated answer

---

## 💻 Frontend

- Built with React (served via Nginx)
- Axios used for API integration
- Highlights are grouped by category and shown with metadata like frequency and source

---

## 📁 Directory Structure

```
ai-news-aggregator-chatbot/
├── backend/              ← FastAPI API & pipeline scripts
│   ├── api/              ← main.py (FastAPI app)
│   ├── scraper/          ← Raw scraping logic
│   ├── config.py         ← Shared constants & model paths
│   └── start.py          ← Starts FastAPI server
├── frontend/             ← React app (build via Docker)
├── docker-compose.yml    ← Runs backend + frontend
```

---

## 📬 Submission Instructions
- Submit GitHub link + deployed URL (if any) to `info@foboh.com.au`
- README must include instructions to run backend, pipeline, and frontend
- Tests are optional, but bonus points if provided

---

## 🧠 Credits
- Developed for Foboh AI Challenge
- Built by Nauman Mansuri
