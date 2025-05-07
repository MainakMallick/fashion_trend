from fastapi import FastAPI
import subprocess
import json
import os
from mongo_db import get_trends

app = FastAPI()

@app.get("/scrape")
def scrape(query: str = "streetwear", scrolls: int = 2):
    try:
        subprocess.run(["python", "scrape_runner.py"], check=True)
        with open("fashion_pinterest_data.json", "r") as f:
            data = json.load(f)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@app.get("/trends")
def trends_api(query: str = None, source: str = None, limit: int = 10):
    return get_trends(query=query, source=source, limit=limit)
