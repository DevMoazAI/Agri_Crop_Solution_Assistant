# llm_parser.py
import os
import json
import re

# Load crop and disease keywords from JSON
file_path = os.path.join(os.path.dirname(__file__), "data/crop_and_diseases.json")

with open(file_path, "r", encoding="utf-8") as f:
    agri_map = json.load(f)

def normalize(text):
    return re.sub(r"\s+", "", text.lower())

def extract_crop_disease(query):
    crop_found, disease_found = None, None
    q = normalize(query)

    for crop in agri_map['crops']:
        if normalize(crop) in q:
            crop_found = crop
            break

    for disease in agri_map['diseases']:
        if normalize(disease) in q:
            disease_found = disease
            break

    return crop_found, disease_found