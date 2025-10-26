from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Allow frontend access (React Native, Web, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to med.json file
json_path = os.path.join(os.path.dirname(__file__), "med.json")

# Load the medicine data
with open(json_path, "r", encoding="utf-8") as f:
    med_data = json.load(f)


@app.get("/")
def home():
    return {"message": "Welcome to the Medicine API"}


@app.get("/medicines")
def get_all_medicines():
    """Return all medicine data"""
    return med_data


@app.get("/medicines/{category}")
def get_medicines_by_category(category: str):
    """Return medicines filtered by category"""
    category = category.lower()
    if category in med_data["MEDICINES_BY_TYPE"]:
        return {
            "category": category,
            "items": med_data["MEDICINES_BY_TYPE"][category],
        }
    else:
        return {"error": "Category not found"}
