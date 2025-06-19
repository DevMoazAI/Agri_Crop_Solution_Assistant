
# app.py (main entry point for Streamlit app)

import streamlit as st
# from llm_parser import extract_crop_disease  # No longer used
from db.db_query import query_agri_data
from agri_keywords import is_agri_related
from llm_query import get_response_from_llm
import pandas as pd

st.set_page_config(page_title="Agri Crop Advisor")
st.title(" Agri Crop Solution Assistant")

user_input = st.text_input("Ask about a crop issue (English,Roman Urdu):")

if user_input:
    if not is_agri_related(user_input):
        st.error("This query doesn't seem related to agriculture.")
    else:
        llm_response = get_response_from_llm(user_input)

        st.text(f"DEBUG: LLM response type: {llm_response.get('type')}")

        if llm_response["type"] == "non-agri":
            st.error(llm_response["message"])

        elif llm_response["type"] == "agri-fallback":
            st.warning("Trying intelligent extraction using LLM...")
            st.info("Could not match specific crop/disease. Here's general advice:")

            general_info = llm_response["message"]

            if "|" in general_info and "---" in general_info:
                try:
                    parts = general_info.split("\n\n", 1)
                    st.markdown(parts[0])  # disease points
                    st.markdown("### Suggested Medicines (from LLM)")
                    st.markdown(parts[1], unsafe_allow_html=True)
                except Exception:
                    st.markdown(general_info)
            else:
                st.markdown(general_info)
            
        elif llm_response["type"] == "agri-match":
            crop = llm_response.get("crop")
            disease = llm_response.get("disease")

            # print(f" LLM returned: crop={crop}, disease={disease}")

            st.success(f"Identified: {crop} / {disease}")
            st.markdown("### Disease Information")
            points = llm_response.get("points", [])
            if isinstance(points, list):
                for i, point in enumerate(points, start=1):
                    st.markdown(f"**{i}.** {point}")
            else:
                st.warning("Unexpected format for points. Skipping disease information display.")
                st.code(str(points))

            # for i, point in enumerate(llm_response.get("points", []), start=1):
            #     st.markdown(f"**{i}.** {point}")

            products = query_agri_data(crop=crop, disease=disease)  # from db_query.py
            # if products:
            #     st.markdown("### Raw DB Result")
            #     st.json(products)  # shows raw data in a readable JSON format
            # else:
            #     st.warning("No medicines found for this crop-disease combination.")

            if products:
                st.markdown("### Medicines")

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
                st.warning("No medicines found for this crop-disease combination.")

