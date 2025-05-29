from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import os

app = FastAPI()

# Enable CORS so frontend can call API from localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load highlights from file
def load_highlights():
    highlights_path = os.path.join("data", "highlights.json")
    print("highlights_path", highlights_path)
    if os.path.exists(highlights_path):
        with open(highlights_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.get("/api/highlights")
def get_highlights():
    with open("data/highlights.json", "r", encoding="utf-8") as f:
        return json.load(f)  # ✅ Return a list directly


@app.get("/")
def root():
    return {"message": "News Highlights API is running."}
