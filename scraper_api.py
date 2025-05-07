from fastapi import FastAPI
import subprocess
import json
import os

app = FastAPI()

@app.get("/scrape")
def scrape(query: str = "streetwear", scrolls: int = 2):
    try:
        subprocess.run(["python", "scrape_runner.py"], check=True)
        with open("scraped_data.json", "r") as f:
            data = json.load(f)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
