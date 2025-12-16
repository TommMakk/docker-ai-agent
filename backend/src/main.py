import os
from fastapi import FastAPI



app = FastAPI()


MY_PROJECT = os.environ.get("MY_PROJECT") or "This is my project"
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set")
@app.get("/")
def read_index():
    return {"hello": "world nowww!", "project_name": MY_PROJECT, "api_key": API_KEY}
