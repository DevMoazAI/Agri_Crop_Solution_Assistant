# db_query.py

import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def query_agri_data(crop=None, disease=None, fallback_query=None):
    """
    Queries Supabase for agriculture-related data based on crop and disease.
    Returns a list of matched records (products).
    """

    crop = crop.strip().lower() if crop else None
    disease = disease.strip().lower() if disease else None

    # Debug: print sample crop-disease pairs
    try:
        all_rows = supabase.table("agri_companies_data").select("crop", "disease").limit(10).execute()
        for row in all_rows.data:
            print(f" Crop: {row['crop']} | Disease: {row['disease']}")
    except Exception as e:
        print("Error fetching sample data:", e)

    # Main query
    if crop and disease:
        response = supabase.table("agri_companies_data").select("*") \
            .ilike("crop", f"%{crop}%") \
            .ilike("disease", f"%{disease}%") \
            .execute()

    elif fallback_query:
        fallback_query = fallback_query.strip().lower()
        response = supabase.table("agri_companies_data") \
            .select("*") \
            .ilike("crop", f"%{fallback_query}%") \
            .execute()
    else:
        return []

    # Clean price values
    for item in response.data:
        try:
            item["price_pkr"] = int(str(item["price_pkr"]).replace(",", "").replace("PKR", "").strip())
        except:
            pass

    return response.data






























# import os
# from supabase import create_client
# from dotenv import load_dotenv

# load_dotenv()

# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# # FIX: Assign the client to a variable
# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# def query_agri_data(crop=None, disease=None, fallback_query=None):
#     #  Normalize input
#     crop = crop.strip().lower() if crop else None
#     disease = disease.strip().lower() if disease else None
# # Print available crops and diseases in DB
#     all_rows = supabase.table("agri_companies_data").select("crop", "disease").limit(10).execute()
#     # print(" Sample crops/diseases in DB:")
#     for row in all_rows.data:
#         print(f" Crop: {row['crop']} | Disease: {row['disease']}")
              
#     if crop and disease:
#         # Query with ILIKE (case-insensitive)
#         crop = crop.strip().lower()
#         disease = disease.strip().lower()
#         response = supabase.table("agri_companies_data").select("*") \
#             .ilike("crop", f"%{crop}%") \
#             .ilike("disease", f"%{disease}%") \
#             .execute()

#     elif fallback_query:
#         fallback_query = fallback_query.strip().lower()
#         response = supabase.table("agri_companies_data") \
#             .select("*") \
#             .ilike("crop", f"%{fallback_query}%") \
#             .execute()
#     else:
#         return []

#     # print(f" DB Response: {response.data}")

#     # Optional: Clean price
#     for item in response.data:
#         try:
#             item["price_pkr"] = int(str(item["price_pkr"]).replace(",", "").replace("PKR", "").strip())
#         except:
#             pass

#     return response.data