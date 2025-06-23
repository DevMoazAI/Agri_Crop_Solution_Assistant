
# # app.py (main entry point for Streamlit app)


import streamlit as st
from db.db_query import query_agri_data
from agri_keywords import is_agri_related
from llm_query import get_response_from_llm
import pandas as pd

st.set_page_config(page_title="Agri Crop Advisor")
st.title(" Agri Crop Solution Assistant")

user_input = st.text_input("Ask about a crop issue (English, Roman Urdu):")

if user_input:
    if not is_agri_related(user_input):
        st.error(" This query doesn't seem related to agriculture.")
    else:
        llm_response = get_response_from_llm(user_input)

        if llm_response["type"] == "non-agri":
            st.error(llm_response["message"])

        elif llm_response["type"] == "agri-fallback":
            st.warning(" Partial match: Disease identified, but crop name is missing.")

            if "points" in llm_response:
                st.markdown("### Disease Information")
                for i, point in enumerate(llm_response["points"], start=1):
                    st.markdown(f"**{i}.** {point}")

            st.markdown(" Please specify the crop name to get medicine info:")
            crop_name = st.text_input("Enter crop name:", key="ask_crop")

            if crop_name:
                from llm_query import recent_context
                disease = recent_context.get("disease")
                if disease:
                    db_results = query_agri_data(crop_name, disease)
                    if db_results:
                        st.success(f" Crop: {crop_name} / Disease: {disease}")
                        st.markdown("### Recommended Medicines:")
                        df = pd.DataFrame(db_results)
                        st.dataframe(df)
                    else:
                        st.warning(" No medicine found for this crop-disease combination.")
                else:
                    st.error("Something went wrong — disease context missing.")

            general_info = llm_response["message"]

            # Show additional explanation only if it's not a raw JSON object
            if general_info and not general_info.strip().startswith("{"):
                st.markdown("---")
                st.markdown("#### Additional Info")
                st.markdown(general_info)

        elif llm_response["type"] == "agri-match":
            crop = llm_response.get("crop")
            disease = llm_response.get("disease")

            st.success(f" Identified: {crop} / {disease}")

            points = llm_response.get("points", [])
            if isinstance(points, list) and points:
                st.markdown("### Disease Information")
                for i, point in enumerate(points, start=1):
                    st.markdown(f"**{i}.** {point}")
            else:
                st.warning(" Disease info not available in structured format.")

            products = query_agri_data(crop=crop, disease=disease)
            if products:
                st.markdown("### Recommended Medicines")

                df = pd.DataFrame(products)
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
                st.dataframe(df, use_container_width=True)
            else:
                st.warning(" No medicines found for this crop-disease combination.")
