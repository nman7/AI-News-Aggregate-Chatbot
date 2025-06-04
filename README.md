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

A step-by-step guide to run the AI News Aggregator & Chatbot locally using Docker.

---

### 🧹 Step 1: Clean Existing Containers (Optional – if restarting from scratch)
```bash
# Stop and remove all running containers
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)

# Optionally remove all local Docker images
docker rmi $(docker images -q) --force
```

---

### 🏗️ Step 2: Build and Start Backend + Frontend Containers
```bash
docker-compose up --build
```

- This will build and launch both the backend (FastAPI) and frontend (React via Nginx).
- The backend logs should include:
  ```
  🚀 Starting FastAPI backend...
  ```

⚠️ **Note:** The backend server will not fully function until the pipeline is run once.

---

### ⚙️ Step 3: Run the Data Pipeline Inside Backend Container (Only First Time)
```bash
# Access the backend container shell
docker exec -it news-backend bash

# Run the pipeline to scrape news, summarize articles, and build FAISS index
python pipeline.py
```

📋 Sample Logs:
```
🧠 Loading summarization model...
✅ Completed Batch #1
📌 Highlights saved to combined_articles_with_summary_highlights.json
✅ FAISS index and metadata saved to rag_index/
```

---

### 🔁 Step 4: Restart Backend to Load Data
```bash
docker restart news-backend
```

---

### 🌐 Access the Application
- Frontend UI: [http://localhost:3000](http://localhost:3000)
- API: [http://localhost:8000](http://localhost:8000/docs)

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
## Screenshot

<img width="1512" alt="Screenshot 2025-06-04 at 10 47 13 PM" src="https://github.com/user-attachments/assets/7760794a-2e3c-4c8f-b59b-b3ff26f5115e" />

---
##  Youtube Link
[Watch the demo video](https://www.youtube.com/watch?v=lXs2cByzz54)
