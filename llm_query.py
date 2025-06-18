import os
import json
import re
import requests
from db.db_query import query_agri_data
from prompt import SYSTEM_PROMPT

# Load environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_ENDPOINT = os.getenv("GROQ_API_ENDPOINT")
MODEL_NAME = os.getenv("MODEL_NAME")

def safe_extract_json(text):
    """
    Extracts the first valid JSON object from a text string by tracking braces.
    """
    start = text.find('{')
    if start == -1:
        return None, "No opening brace '{' found."

    brace_count = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            brace_count += 1
        elif text[i] == '}':
            brace_count -= 1

        if brace_count == 0:
            json_str = text[start:i+1]
            try:
                parsed = json.loads(json_str)
                return parsed, None
            except json.JSONDecodeError as e:
                return None, f"JSON decode error: {str(e)}"

    return None, "Braces did not match properly in the text."


def get_response_from_llm(user_query):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    }

    try:
        response = requests.post(GROQ_API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        content = result["choices"][0]["message"]["content"].strip()

        print("Raw LLM Content:\n", content)

        llm_json, error = safe_extract_json(content)
        if error:
            print("JSON parsing error:", error)
            return {
                "type": "error",
                "error": f"Invalid JSON in LLM response: {error}",
                "raw_response": content
            }

        llm_json.setdefault("points", [])
        llm_json.setdefault("products", [])

        # Also get explanation part (if any)
        json_part = json.dumps(llm_json)
        explanation_part = content.replace(json_part, '').strip()

        if not llm_json.get("is_agriculture", False):
            return {
                "type": "non-agri",
                "message": "Main sirf zaraat se mutaliq sawalat ke jawab deta hoon."
            }

        # Extract crop & disease
        crop = llm_json.get("crop", "fallback")
        disease = llm_json.get("disease", "fallback")

        if crop == "fallback" or disease == "fallback":
            return {
                "type": "agri-fallback",
                "message": explanation_part
            }
        # Query database for matching medicine info
        db_results = query_agri_data(crop, disease)
        print(" DB Query Result:\n", db_results)
        return {
            "type": "agri-match",
            "crop": crop,
            "disease": disease,
            "points": llm_json.get("points", []),
            "message": explanation_part,
            "products": db_results
        }

    except requests.exceptions.RequestException as e:
        print("API request failed:", e)
        return {
            "type": "error",
            "error": "API call failed",
            "raw_response": str(e)
        }