import os
import json
import requests
from db.db_query import query_agri_data
from prompt import SYSTEM_PROMPT

# Load environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_ENDPOINT = os.getenv("GROQ_API_ENDPOINT")
MODEL_NAME = os.getenv("MODEL_NAME")

# Memory for context
recent_context = {"crop": None, "disease": None}

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
            return {
                "type": "error",
                "error": f"Invalid JSON in LLM response: {error}",
                "raw_response": content
            }

        llm_json.setdefault("points", [])
        crop = llm_json.get("crop", "fallback")
        disease = llm_json.get("disease", "fallback")

        # Update context if available
        if crop != "fallback":
            recent_context["crop"] = crop
        if disease != "fallback":
            recent_context["disease"] = disease

        json_part = json.dumps(llm_json)
        explanation_part = content.replace(json_part, '').strip()

        if not llm_json.get("is_agriculture", False):
            return {
                "type": "non-agri",
                "message": "Main sirf zaraat se mutaliq sawalat ke jawab deta hoon."
            }
        
        # 👉 New block: If it's agri-related but no crop or disease is found
        if llm_json.get("is_agriculture", False) and crop == "fallback" and disease == "fallback" and not llm_json.get("points") == []:
            return {
                "type": "agri-general",
                "message": explanation_part,
                "points": llm_json.get("points", [])
            }

        # Fallback logic using memory
        # if crop == "fallback" and recent_context["crop"]:
        #     crop = recent_context["crop"]
        # if disease == "fallback" and recent_context["disease"]:
        #     disease = recent_context["disease"]
        # Use previous context only if BOTH crop and disease are missing
        if crop == "fallback" and disease == "fallback":
            if recent_context["crop"]:
                crop = recent_context["crop"]
            if recent_context["disease"]:
                disease = recent_context["disease"]

        # Final fallback: still missing crop or disease
        if crop == "fallback" or disease == "fallback":
            return {
                "type": "agri-fallback",
                "message": explanation_part,
                "points": llm_json.get("points", [])
            }

        # Full match: crop + disease
        db_results = query_agri_data(crop, disease)
        return {
            "type": "agri-match",
            "crop": crop,
            "disease": disease,
            "points": llm_json.get("points", []),
            "message": explanation_part,
            "products": db_results
        }

    except requests.exceptions.RequestException as e:
        return {
            "type": "error",
            "error": "API call failed",
            "raw_response": str(e)
        }
