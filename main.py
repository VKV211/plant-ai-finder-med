from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React app access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load med.json
json_path = os.path.join(os.path.dirname(__file__), "med.json")

with open(json_path, "r", encoding="utf-8") as f:
    med_data = json.load(f)


@app.get("/")
def home():
    return {"message": "Medicine API Running 🚀"}


@app.get("/search")
def search_medicine(query: str = Query(..., description="Disease or type or name")):
    """Search medicines by disease type or disease name"""

    query = query.lower().strip()

    # Check if it's a known medicine type directly
    if query in med_data["MEDICINES_BY_TYPE"]:
        return med_data["MEDICINES_BY_TYPE"][query]

    # Otherwise, find which disease type contains the disease name
    for disease_type, diseases in med_data["DISEASE_BY_TYPE"].items():
        for disease in diseases:
            if query in disease.lower():
                return med_data["MEDICINES_BY_TYPE"].get(disease_type, [])

    # If not found
    return {"message": "No medicines found for this search."}
