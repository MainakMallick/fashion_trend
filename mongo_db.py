import json
from pymongo import MongoClient
from datetime import datetime

# 1. Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["fashion_trends"]
collection = db["trends"]

# 2. Define a helper to insert with metadata
def insert_trends(trends, query, source):
    for trend in trends:
        trend["query"] = query
        trend["source"] = source
        trend["created_at"] = datetime.utcnow()
    collection.insert_many(trends)
    print(f"✅ Inserted {len(trends)} items from {source}.")

# 3. Load and insert Pinterest data
try:
    with open("fashion_pinterest_data.json", "r", encoding="utf-8") as f:
        pinterest_data = json.load(f)
    insert_trends(pinterest_data, query="fashion", source="pinterest")
except Exception as e:
    print(f"⚠️ Error loading Pinterest data: {e}")

# 4. Load and insert Reddit data
try:
    with open("fashion_reddit_data.json", "r", encoding="utf-8") as f:
        reddit_data = json.load(f)
    insert_trends(reddit_data, query="fashion", source="reddit")
except Exception as e:
    print(f"⚠️ Error loading Reddit data: {e}")

def get_trends(query=None, source=None, limit=10):
    filter_query = {}
    if query:
        filter_query["query"] = query
    if source:
        filter_query["source"] = source

    cursor = collection.find(filter_query).sort("created_at", -1).limit(limit)
    trends = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string for JSON
        trends.append(doc)
    return trends
