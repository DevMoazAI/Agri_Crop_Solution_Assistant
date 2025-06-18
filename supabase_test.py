# SUPABASE_URL=https://acejydnizhuczogfjofa.supabase.co
# SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFjZWp5ZG5pemh1Y3pvZ2Zqb2ZhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk5MTMyNzMsImV4cCI6MjA2NTQ4OTI3M30.kun7zzRZkvoKduJkwC6U2ltS_thH3xmzpvK1D_UfH1I

from supabase import create_client, Client

# Replace with your actual Supabase credentials
SUPABASE_URL="https://acejydnizhuczogfjofa.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFjZWp5ZG5pemh1Y3pvZ2Zqb2ZhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk5MTMyNzMsImV4cCI6MjA2NTQ4OTI3M30.kun7zzRZkvoKduJkwC6U2ltS_thH3xmzpvK1D_UfH1I"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def test_connection():
    print("Testing Supabase connection and fetching sample data...")

    try:
        response = supabase.table("agri_companies_data").select("*").limit(5).execute()
        print("Connection successful.\n")

        if not response.data:
            print("The table is currently empty.")
        else:
            print("Sample records:")
            for row in response.data:
                print(f"- Crop: {row.get('crop')}, Disease: {row.get('disease')}, Product: {row.get('trade_name')}")
    except Exception as e:
        print("Error connecting to Supabase or fetching data:")
        print(e)


def insert_sample_data():
    print("Inserting test data into agri_companies_data table...")

    data = {
        "trade_name": "Blight Buster",
        "generic_name": "Copper Hydroxide",
        "crop": "Vegetables",
        "disease": "Blight",
        "dose_per_acre": "500ml",
        "company": "GreenAgri",
        "category": "Fungicide",
        "price_pkr": 750,
        "efficacy_test_result": "92% in 2 weeks"
    }

    try:
        response = supabase.table("agri_companies_data").insert(data).execute()
        print("Test data inserted successfully.")
    except Exception as e:
        print("Error inserting data:")
        print(e)


if __name__ == "__main__":
    test_connection()

    user_input = input("\nDo you want to insert a test record? (yes/no): ").strip().lower()
    if user_input in ("yes", "y"):
        insert_sample_data()
