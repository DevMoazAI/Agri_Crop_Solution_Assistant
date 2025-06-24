# agri_keywords.py
import os
import json
from rapidfuzz import fuzz, process

# Paths
base_dir = os.path.dirname(__file__)
crop_file_path = os.path.join(base_dir, "data/crop_and_diseases.json")
keyword_file_path = os.path.join(base_dir, "data/agri_keywords.json")

# Load crop and disease data
with open(crop_file_path, "r", encoding="utf-8") as f:
    crop_data = json.load(f)

# Load general agri-related keywords
with open(keyword_file_path, "r", encoding="utf-8") as f:
    keyword_data = json.load(f)

# Combine all words into one list for fuzzy matching
AGRI_KEYWORDS = set(
    word.lower()
    for word in crop_data["crops"]
    + crop_data["diseases"]
    + keyword_data["general_agri_terms"]
)

AGRI_KEYWORDS_LIST = list(AGRI_KEYWORDS)

# Fuzzy match check (threshold 80%)
# def is_agri_related(query: str, threshold: int = 80) -> bool:
#     query_words = query.lower().split()

#     for word in query_words:
#         match, score, _ = process.extractOne(word, AGRI_KEYWORDS_LIST, scorer=fuzz.ratio)
#         if score >= threshold:
#             return True
#     return False
# Load keyword data
with open(keyword_file_path, "r", encoding="utf-8") as f:
    keyword_data = json.load(f)

greeting_keywords = keyword_data.get("greetings", [])
general_agri_terms = keyword_data.get("general_agri_terms", [])

# Fuzzy matching list
AGRI_KEYWORDS = set(
    word.lower()
    for word in crop_data["crops"]
    + crop_data["diseases"]
    + general_agri_terms
)
AGRI_KEYWORDS_LIST = list(AGRI_KEYWORDS)

# Include greetings check in agri check
def is_agri_related(query: str, threshold: int = 80) -> bool:
    query_lower = query.lower()

    # First allow greeting-based queries
    if any(greet in query_lower for greet in greeting_keywords):
        return True

    # Then check agri terms using fuzzy match
    for word in query_lower.split():
        match, score, _ = process.extractOne(word, AGRI_KEYWORDS_LIST, scorer=fuzz.ratio)
        if score >= threshold:
            return True

    return False
