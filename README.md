# 📰 AI News Aggregator & Chatbot

A full-stack AI-powered system that scrapes Australian news, summarizes daily highlights, and answers user questions using RAG (Retrieval-Augmented Generation).

## ⚙️ Tech Stack

- **Backend**: FastAPI, HuggingFace Transformers, FAISS
- **Frontend**: React + Axios
- **Scraper**: Requests + BeautifulSoup
- **DevOps**: Docker, Docker Compose

## ✅ Features

- Scrapes news from ABC, The Guardian, and The New Daily
- Summarizes and highlights news by category (sports, finance, lifestyle, music)
- Detects duplicates using frequency and keywords
- RAG chatbot answers user questions using FAISS search + text generation
- Clean frontend UI to display highlights

## 🚀 Quick Start (Docker)

```bash
# 1. Remove old containers/images (if needed)
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q) --force

# 2. Build & run the app
docker-compose up --build


# 3. Run pipeline manually
docker exec -it news-backend bash

# Run news extraction + processing pipeline
python pipeline.py
