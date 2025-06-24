# app_logic.py
import pandas as pd
# Assuming db.db_query and agri_keywords are in sibling directories/files
# Adjust these imports based on your actual project structure if needed
from db.db_query import query_agri_data
from agri_keywords import is_agri_related
from llm_query import get_response_from_llm
# Ensure recent_context is handled properly; if it's a global, reconsider for multi-user
# For single-user local app, this import might still work if recent_context is defined in llm_query.py
from llm_query import recent_context


def process_user_input(user_input, crop_name_input=""):
    """Main function to process user input - contains your existing logic"""

    if not user_input:
        return "Please enter a question about crops.", None, None

    # Your existing logic starts here
    if not is_agri_related(user_input):
        return "ERROR: This query doesn't seem related to agriculture.", None, None

    llm_response = get_response_from_llm(user_input)

    if llm_response["type"] == "non-agri":
        return f"ERROR: {llm_response['message']}", None, None

    elif llm_response["type"] == "agri-fallback":
        response_text = "WARNING: Partial match: Disease identified, but crop name is missing.\n\n"

        if "points" in llm_response:
            response_text += "### Disease Information\n"
            for i, point in enumerate(llm_response["points"], start=1):
                response_text += f"**{i}.** {point}\n"

        response_text += "\n**Please specify the crop name below to get medicine info:**"

        # Handle crop name input if provided
        medicine_data = None
        if crop_name_input:
            # Assuming recent_context correctly holds the disease from the previous LLM call
            disease = recent_context.get("disease")
            if disease:
                db_results = query_agri_data(crop_name_input, disease)
                if db_results:
                    response_text += f"\n\n Crop: {crop_name_input} / Disease: {disease}\n"
                    response_text += "### Recommended Medicines:\n"

                    df = pd.DataFrame(db_results)
                    medicine_data = _format_medicine_dataframe(df) # Use helper function
                else:
                    response_text += f"\n\n No medicine found for {crop_name_input}-{disease} combination."
            else:
                response_text += "\n\n Something went wrong — disease context missing."

        general_info = llm_response["message"]
        if general_info and not general_info.strip().startswith("{"):
            response_text += f"\n\n---\n#### Additional Info\n{general_info}"

        # Return a flag to indicate if crop input should be shown
        show_crop_input_flag = True # Set this to True for the fallback case
        return response_text, show_crop_input_flag, medicine_data

    elif llm_response["type"] == "agri-general":
        response_text = "SUCCESS: General Agriculture Question Detected\n\n### Information\n"
        for i, point in enumerate(llm_response.get("points", []), start=1):
            response_text += f"**{i}.** {point}\n"

        return response_text, False, None # No crop input needed for general agri questions

    elif llm_response["type"] == "agri-match":
        crop = llm_response.get("crop")
        disease = llm_response.get("disease")

        response_text = f"SUCCESS: Identified: {crop} / {disease}\n\n"

        points = llm_response.get("points", [])
        if isinstance(points, list) and points:
            response_text += "### Disease Information\n"
            for i, point in enumerate(points, start=1):
                response_text += f"**{i}.** {point}\n"
        else:
            response_text += "WARNING: Disease info not available in structured format.\n"

        products = query_agri_data(crop=crop, disease=disease)
        medicine_data = None

        if products:
            response_text += "\n### Recommended Medicines\n"
            df = pd.DataFrame(products)
            medicine_data = _format_medicine_dataframe(df) # Use helper function
        else:
            response_text += "\nWARNING: No medicines found for this crop-disease combination."

        return response_text, False, medicine_data # No crop input needed for full match

    return "Something went wrong. Please try again.", False, None

def _format_medicine_dataframe(df):
    """Helper function to format the medicine DataFrame."""
    df = df[
        ["trade_name", "generic_name", "crop", "disease", "dose_per_acre",
         "company", "category", "price_pkr", "efficacy_test_result"]
    ]
    df.rename(columns={
        "trade_name": "Trade Name",
        "generic_name": "Generic Name",
        "crop": "Crop",
        "disease": "Disease",
        "dose_per_acre": "Dose per Acre",
        "company": "Company",
        "category": "Category",
        "price_pkr": "Price (PKR)",
        "efficacy_test_result": "Efficacy"
    }, inplace=True)

    def format_price(x):
        try:
            return f"PKR {int(x):,}"
        except:
            return str(x)

    df["Price (PKR)"] = df["Price (PKR)"].apply(format_price)
    return df