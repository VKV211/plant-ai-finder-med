from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="Medicine Recommendation API", version="1.0")

# Allow frontend (React) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load med.json data
BASE_DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(BASE_DIR, "med.json")

try:
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        med_data = json.load(f)
except Exception as e:
    med_data = {"error": f"Failed to load med.json: {str(e)}"}


@app.get("/")
def home():
    """Root endpoint to verify API is running"""
    return {"message": "🚀 Medicine API Running Successfully!"}


@app.get("/search")
def search_medicine(query: str = Query(..., description="Search by disease name or type")):
    """Search for medicines by disease type or disease name"""

    query = query.lower().strip()

    # Check if query matches a known medicine type
    if query in med_data.get("MEDICINES_BY_TYPE", {}):
        return {"query": query, "results": med_data["MEDICINES_BY_TYPE"][query]}

    # Otherwise, search inside disease types for a match
    for disease_type, diseases in med_data.get("DISEASE_BY_TYPE", {}).items():
        for disease in diseases:
            if query in disease.lower():
                medicines = med_data["MEDICINES_BY_TYPE"].get(disease_type, [])
                return {"query": query, "results": medicines}

    # If no matches found
    return {"query": query, "message": "❌ No medicines found for this search."}


# Run the app with Uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
