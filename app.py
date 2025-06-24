# app.py (Gradio version - keeping your existing logic intact)

import gradio as gr
from db.db_query import query_agri_data
from agri_keywords import is_agri_related
from llm_query import get_response_from_llm
import pandas as pd

def process_user_input(user_input, crop_name_input=""):
    """Main function to process user input - contains your existing logic"""
    
    if not user_input:
        return "Please enter a question about crops.", "", None
    
    # Your existing logic starts here
    if not is_agri_related(user_input):
        return "ERROR: This query doesn't seem related to agriculture.", "", None
    
    llm_response = get_response_from_llm(user_input)
    
    if llm_response["type"] == "non-agri":
        return f"ERROR: {llm_response['message']}", "", None
    
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
            from llm_query import recent_context
            disease = recent_context.get("disease")
            if disease:
                db_results = query_agri_data(crop_name_input, disease)
                if db_results:
                    response_text += f"\n\n Crop: {crop_name_input} / Disease: {disease}\n"
                    response_text += "### Recommended Medicines:\n"
                    
                    df = pd.DataFrame(db_results)
                    medicine_data = df
                else:
                    response_text += f"\n\n No medicine found for {crop_name_input}-{disease} combination."
            else:
                response_text += "\n\n Something went wrong — disease context missing."
        
        general_info = llm_response["message"]
        if general_info and not general_info.strip().startswith("{"):
            response_text += f"\n\n---\n#### Additional Info\n{general_info}"
        
        return response_text, "", medicine_data
    
    elif llm_response["type"] == "agri-general":
        response_text = "SUCCESS: General Agriculture Question Detected\n\n### Information\n"
        for i, point in enumerate(llm_response.get("points", []), start=1):
            response_text += f"**{i}.** {point}\n"
        
        return response_text, "", None
    
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
            medicine_data = df
        else:
            response_text += "\nWARNING: No medicines found for this crop-disease combination."
        
        return response_text, "", medicine_data
    
    return "Something went wrong. Please try again.", "", None

def handle_crop_name_submission(user_input, crop_name):
    """Handle when user submits crop name for fallback case"""
    return process_user_input(user_input, crop_name)

# Custom CSS for professional styling
custom_css = """
/* Main container styling */
.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 20px;
}

/* Desktop layout - proper website look */
@media (min-width: 1024px) {
    .gradio-container {
        padding: 40px;
    }
    
    .main-content {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30px;
        align-items: start;
    }
    
    .input-section {
        padding-right: 20px;
    }
    
    .response-section {
        padding-left: 20px;
        border-left: 2px solid #e0e0e0;
    }
}

/* Header styling */
.main-header {
    background: linear-gradient(135deg, #2c5530 0%, #3d7c47 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    text-align: center;
}

/* Status message styling */
.status-error {
    color: #d32f2f;
    font-weight: 600;
    background-color: #ffebee;
    padding: 10px;
    border-left: 4px solid #d32f2f;
    border-radius: 4px;
    margin: 10px 0;
}

.status-warning {
    color: #f57c00;
    font-weight: 600;
    background-color: #fff3e0;
    padding: 10px;
    border-left: 4px solid #f57c00;
    border-radius: 4px;
    margin: 10px 0;
}

.status-success {
    color: #388e3c;
    font-weight: 600;
    background-color: #e8f5e8;
    padding: 10px;
    border-left: 4px solid #388e3c;
    border-radius: 4px;
    margin: 10px 0;
}

/* Button styling */
.primary-btn {
    background: linear-gradient(135deg, #2c5530 0%, #3d7c47 100%) !important;
    color: white !important;
    border: none !important;
    padding: 12px 24px !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.primary-btn:hover {
    background: linear-gradient(135deg, #1b3a1f 0%, #2d5e36 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(44, 85, 48, 0.3) !important;
}

.secondary-btn {
    background: #f5f5f5 !important;
    color: #666 !important;
    border: 1px solid #ddd !important;
    padding: 12px 24px !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}

.secondary-btn:hover {
    background: #e0e0e0 !important;
    border-color: #bbb !important;
}

/* Input styling */
.input-field {
    border: 2px solid #e0e0e0 !important;
    border-radius: 8px !important;
    padding: 12px !important;
    font-size: 14px !important;
    transition: border-color 0.3s ease !important;
}

.input-field:focus {
    border-color: #3d7c47 !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(61, 124, 71, 0.1) !important;
}

/* Table styling */
.dataframe-container {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Response area styling */
.response-area {
    background: #fafafa;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    min-height: 100px;
    line-height: 1.6;
}

/* Responsive design */
@media (max-width: 1023px) {
    .gradio-container {
        padding: 15px;
    }
    
    .main-header {
        padding: 15px;
    }
    
    .primary-btn, .secondary-btn {
        width: 100% !important;
        margin-bottom: 10px !important;
    }
    
    .main-content {
        display: block !important;
    }
    
    .response-section {
        border-left: none !important;
        padding-left: 0 !important;
        margin-top: 20px;
    }
}
"""

# Create Gradio Interface
with gr.Blocks(title="Agri Crop Advisor", css=custom_css, theme=gr.themes.Base()) as app:
    gr.HTML('<div class="main-header"><h1>Agri Crop Solution Assistant</h1><p>Professional crop disease diagnosis and treatment recommendations</p></div>')
    
    with gr.Row(elem_classes=["main-content"]):
        with gr.Column(scale=1, elem_classes=["input-section"]):
            user_input = gr.Textbox(
                label="Your Question",
                placeholder="Ask about a crop issue (English, Roman Urdu)...",
                lines=4,
                elem_classes=["input-field"]
            )
            
            with gr.Row():
                submit_btn = gr.Button("Submit Question", elem_classes=["primary-btn"])
                clear_btn = gr.Button("Clear", elem_classes=["secondary-btn"])
            
            # Crop name input (for fallback cases)
            crop_name_input = gr.Textbox(
                label="Crop Name (if requested above)",
                placeholder="Enter crop name...",
                visible=False,
                elem_classes=["input-field"]
            )
            crop_submit_btn = gr.Button("Submit Crop Name", visible=False, elem_classes=["primary-btn"])
        
        with gr.Column(scale=1, elem_classes=["response-section"]):
            response_output = gr.HTML(label="Response", elem_classes=["response-area"])
            
            # Medicine data table (conditionally shown)
            medicine_table = gr.Dataframe(
                label="Recommended Medicines",
                visible=False,
                interactive=False,
                elem_classes=["dataframe-container"]
            )

    def format_response_with_styling(response_text):
        """Add CSS classes to status messages for professional styling"""
        
        # Apply styling to status messages
        if response_text.startswith("ERROR:"):
            response_text = f'<div class="status-error">{response_text}</div>'
        elif response_text.startswith("WARNING:"):
            response_text = f'<div class="status-warning">{response_text}</div>'
        elif response_text.startswith("SUCCESS:"):
            response_text = f'<div class="status-success">{response_text}</div>'
        
        # Convert markdown-style text to HTML
        response_text = response_text.replace("### ", "<h3>")
        response_text = response_text.replace("**", "<strong>").replace("**", "</strong>")
        response_text = response_text.replace("\n", "<br>")
        
        return response_text

    def update_interface(user_input, crop_name=""):
        response, _, medicine_data = process_user_input(user_input, crop_name)
        
        # Apply professional styling to response
        styled_response = format_response_with_styling(response)
        
        # Check if we need crop name input (fallback case)
        show_crop_input = "Please specify the crop name below" in response
        show_medicine_table = medicine_data is not None
        
        return (
            styled_response,
            gr.update(visible=show_crop_input),
            gr.update(visible=show_crop_input),
            gr.update(value=medicine_data, visible=show_medicine_table)
        )
    
    def update_interface_with_crop(user_input, crop_name):
        """Handle crop name submission and clear the crop input"""
        response, _, medicine_data = process_user_input(user_input, crop_name)
        
        # Apply professional styling to response
        styled_response = format_response_with_styling(response)
        
        # Always hide crop input after submission and clear it
        show_medicine_table = medicine_data is not None
        
        return (
            styled_response,
            gr.update(visible=False, value=""),  # Hide and clear crop input
            gr.update(visible=False),           # Hide crop submit button
            gr.update(value=medicine_data, visible=show_medicine_table)
        )
    
    def clear_all():
        return "", "", gr.update(visible=False, value=""), gr.update(visible=False), gr.update(visible=False, value=None)
    
    # Event handlers - INSIDE the Blocks context
    submit_btn.click(
        update_interface,
        inputs=[user_input],
        outputs=[response_output, crop_name_input, crop_submit_btn, medicine_table]
    )
    
    crop_submit_btn.click(
        update_interface_with_crop,
        inputs=[user_input, crop_name_input],
        outputs=[response_output, crop_name_input, crop_submit_btn, medicine_table]
    )
    
    clear_btn.click(
        clear_all,
        outputs=[user_input, crop_name_input, crop_name_input, crop_submit_btn, medicine_table]
    )
    
    # Allow Enter key to submit
    user_input.submit(
        update_interface,
        inputs=[user_input],
        outputs=[response_output, crop_name_input, crop_submit_btn, medicine_table]
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",  # Make it accessible from other devices
        server_port=7860,       # Default Gradio port
        share=False,            # Set to True if you want a public link
        debug=True              # Set to False in production
    )


























































# # app.py (Gradio version - keeping your existing logic intact)

# import gradio as gr
# from db.db_query import query_agri_data
# from agri_keywords import is_agri_related
# from llm_query import get_response_from_llm
# import pandas as pd

# def process_user_input(user_input, crop_name_input=""):
#     """Main function to process user input - contains your existing logic"""
    
#     if not user_input:
#         return "Please enter a question about crops.", "", None
    
#     # Your existing logic starts here
#     if not is_agri_related(user_input):
#         return "ERROR: This query doesn't seem related to agriculture.", "", None
    
#     llm_response = get_response_from_llm(user_input)
    
#     if llm_response["type"] == "non-agri":
#         return f"ERROR: {llm_response['message']}", "", None
    
#     elif llm_response["type"] == "agri-fallback":
#         response_text = "WARNING: Partial match: Disease identified, but crop name is missing.\n\n"
        
#         if "points" in llm_response:
#             response_text += "### Disease Information\n"
#             for i, point in enumerate(llm_response["points"], start=1):
#                 response_text += f"**{i}.** {point}\n"
        
#         response_text += "\n**Please specify the crop name below to get medicine info:**"
        
#         # Handle crop name input if provided
#         medicine_data = None
#         if crop_name_input:
#             from llm_query import recent_context
#             disease = recent_context.get("disease")
#             if disease:
#                 db_results = query_agri_data(crop_name_input, disease)
#                 if db_results:
#                     response_text += f"\n\n Crop: {crop_name_input} / Disease: {disease}\n"
#                     response_text += "### Recommended Medicines:\n"
                    
#                     df = pd.DataFrame(db_results)
#                     medicine_data = df
#                 else:
#                     response_text += f"\n\n No medicine found for {crop_name_input}-{disease} combination."
#             else:
#                 response_text += "\n\n Something went wrong — disease context missing."
        
#         general_info = llm_response["message"]
#         if general_info and not general_info.strip().startswith("{"):
#             response_text += f"\n\n---\n#### Additional Info\n{general_info}"
        
#         return response_text, "", medicine_data
    
#     elif llm_response["type"] == "agri-general":
#         response_text = "SUCCESS: General Agriculture Question Detected\n\n### Information\n"
#         for i, point in enumerate(llm_response.get("points", []), start=1):
#             response_text += f"**{i}.** {point}\n"
        
#         return response_text, "", None
    
#     elif llm_response["type"] == "agri-match":
#         crop = llm_response.get("crop")
#         disease = llm_response.get("disease")
        
#         response_text = f"SUCCESS: Identified: {crop} / {disease}\n\n"
        
#         points = llm_response.get("points", [])
#         if isinstance(points, list) and points:
#             response_text += "### Disease Information\n"
#             for i, point in enumerate(points, start=1):
#                 response_text += f"**{i}.** {point}\n"
#         else:
#             response_text += "WARNING: Disease info not available in structured format.\n"
        
#         products = query_agri_data(crop=crop, disease=disease)
#         medicine_data = None
        
#         if products:
#             response_text += "\n### Recommended Medicines\n"
            
#             df = pd.DataFrame(products)
#             df = df[
#                 ["trade_name", "generic_name", "crop", "disease", "dose_per_acre",
#                  "company", "category", "price_pkr", "efficacy_test_result"]
#             ]
#             df.rename(columns={
#                 "trade_name": "Trade Name",
#                 "generic_name": "Generic Name",
#                 "crop": "Crop",
#                 "disease": "Disease",
#                 "dose_per_acre": "Dose per Acre",
#                 "company": "Company",
#                 "category": "Category",
#                 "price_pkr": "Price (PKR)",
#                 "efficacy_test_result": "Efficacy"
#             }, inplace=True)
            
#             def format_price(x):
#                 try:
#                     return f"PKR {int(x):,}"
#                 except:
#                     return str(x)
            
#             df["Price (PKR)"] = df["Price (PKR)"].apply(format_price)
#             medicine_data = df
#         else:
#             response_text += "\nWARNING: No medicines found for this crop-disease combination."
        
#         return response_text, "", medicine_data
    
#     return "Something went wrong. Please try again.", "", None

# def handle_crop_name_submission(user_input, crop_name):
#     """Handle when user submits crop name for fallback case"""
#     return process_user_input(user_input, crop_name)

# # Custom CSS for professional styling
# custom_css = """
# /* Main container styling */
# .gradio-container {
#     max-width: 1200px !important;
#     margin: 0 auto;
#     font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
# }

# /* Header styling */
# .main-header {
#     background: linear-gradient(135deg, #2c5530 0%, #3d7c47 100%);
#     color: white;
#     padding: 20px;
#     border-radius: 10px;
#     margin-bottom: 20px;
#     text-align: center;
# }

# /* Status message styling */
# .status-error {
#     color: #d32f2f;
#     font-weight: 600;
#     background-color: #ffebee;
#     padding: 10px;
#     border-left: 4px solid #d32f2f;
#     border-radius: 4px;
#     margin: 10px 0;
# }

# .status-warning {
#     color: #f57c00;
#     font-weight: 600;
#     background-color: #fff3e0;
#     padding: 10px;
#     border-left: 4px solid #f57c00;
#     border-radius: 4px;
#     margin: 10px 0;
# }

# .status-success {
#     color: #388e3c;
#     font-weight: 600;
#     background-color: #e8f5e8;
#     padding: 10px;
#     border-left: 4px solid #388e3c;
#     border-radius: 4px;
#     margin: 10px 0;
# }

# /* Button styling */
# .primary-btn {
#     background: linear-gradient(135deg, #2c5530 0%, #3d7c47 100%) !important;
#     color: white !important;
#     border: none !important;
#     padding: 12px 24px !important;
#     border-radius: 6px !important;
#     font-weight: 600 !important;
#     transition: all 0.3s ease !important;
# }

# .primary-btn:hover {
#     background: linear-gradient(135deg, #1b3a1f 0%, #2d5e36 100%) !important;
#     transform: translateY(-2px) !important;
#     box-shadow: 0 4px 12px rgba(44, 85, 48, 0.3) !important;
# }

# .secondary-btn {
#     background: #f5f5f5 !important;
#     color: #666 !important;
#     border: 1px solid #ddd !important;
#     padding: 12px 24px !important;
#     border-radius: 6px !important;
#     font-weight: 500 !important;
#     transition: all 0.3s ease !important;
# }

# .secondary-btn:hover {
#     background: #e0e0e0 !important;
#     border-color: #bbb !important;
# }

# /* Input styling */
# .input-field {
#     border: 2px solid #e0e0e0 !important;
#     border-radius: 8px !important;
#     padding: 12px !important;
#     font-size: 14px !important;
#     transition: border-color 0.3s ease !important;
# }

# .input-field:focus {
#     border-color: #3d7c47 !important;
#     outline: none !important;
#     box-shadow: 0 0 0 3px rgba(61, 124, 71, 0.1) !important;
# }

# /* Table styling */
# .dataframe-container {
#     border: 1px solid #e0e0e0;
#     border-radius: 8px;
#     overflow: hidden;
#     box-shadow: 0 2px 4px rgba(0,0,0,0.1);
# }

# /* Response area styling */
# .response-area {
#     background: #fafafa;
#     border: 1px solid #e0e0e0;
#     border-radius: 8px;
#     padding: 20px;
#     min-height: 100px;
#     line-height: 1.6;
# }

# /* Responsive design */
# @media (max-width: 768px) {
#     .gradio-container {
#         padding: 10px;
#     }
    
#     .main-header {
#         padding: 15px;
#     }
    
#     .primary-btn, .secondary-btn {
#         width: 100% !important;
#         margin-bottom: 10px !important;
#     }
# }
# """

# # Create Gradio Interface
# with gr.Blocks(title="Agri Crop Advisor", css=custom_css, theme=gr.themes.Base()) as app:
#     gr.HTML('<div class="main-header"><h1>Agri Crop Solution Assistant</h1><p>Professional crop disease diagnosis and treatment recommendations</p></div>')
    
#     with gr.Row():
#         with gr.Column(scale=2):
#             user_input = gr.Textbox(
#                 label="Your Question",
#                 placeholder="Ask about a crop issue (English, Roman Urdu)...",
#                 lines=3,
#                 elem_classes=["input-field"]
#             )
            
#             with gr.Row():
#                 submit_btn = gr.Button("Submit Question", elem_classes=["primary-btn"])
#                 clear_btn = gr.Button("Clear", elem_classes=["secondary-btn"])
            
#             # Crop name input (for fallback cases)
#             crop_name_input = gr.Textbox(
#                 label="Crop Name (if requested above)",
#                 placeholder="Enter crop name...",
#                 visible=False,
#                 elem_classes=["input-field"]
#             )
#             crop_submit_btn = gr.Button("Submit Crop Name", visible=False, elem_classes=["primary-btn"])
    
#     with gr.Row():
#         with gr.Column():
#             response_output = gr.HTML(label="Response", elem_classes=["response-area"])
            
#             # Medicine data table (conditionally shown)
#             medicine_table = gr.Dataframe(
#                 label="Recommended Medicines",
#                 visible=False,
#                 interactive=False,
#                 elem_classes=["dataframe-container"]
#             )

#     def format_response_with_styling(response_text):
#         """Add CSS classes to status messages for professional styling"""
        
#         # Apply styling to status messages
#         if response_text.startswith("ERROR:"):
#             response_text = f'<div class="status-error">{response_text}</div>'
#         elif response_text.startswith("WARNING:"):
#             response_text = f'<div class="status-warning">{response_text}</div>'
#         elif response_text.startswith("SUCCESS:"):
#             response_text = f'<div class="status-success">{response_text}</div>'
        
#         # Convert markdown-style text to HTML
#         response_text = response_text.replace("### ", "<h3>")
#         response_text = response_text.replace("**", "<strong>").replace("**", "</strong>")
#         response_text = response_text.replace("\n", "<br>")
        
#         return response_text

#     def update_interface(user_input, crop_name=""):
#         response, _, medicine_data = process_user_input(user_input, crop_name)
        
#         # Apply professional styling to response
#         styled_response = format_response_with_styling(response)
        
#         # Check if we need crop name input (fallback case)
#         show_crop_input = "Please specify the crop name below" in response
#         show_medicine_table = medicine_data is not None
        
#         return (
#             styled_response,
#             gr.update(visible=show_crop_input),
#             gr.update(visible=show_crop_input),
#             gr.update(value=medicine_data, visible=show_medicine_table)
#         )
    
#     def clear_all():
#         return "", "", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False, value=None)
    
#     # Event handlers - INSIDE the Blocks context
#     submit_btn.click(
#         update_interface,
#         inputs=[user_input],
#         outputs=[response_output, crop_name_input, crop_submit_btn, medicine_table]
#     )
    
#     crop_submit_btn.click(
#         update_interface,
#         inputs=[user_input, crop_name_input],
#         outputs=[response_output, crop_name_input, crop_submit_btn, medicine_table]
#     )
    
#     clear_btn.click(
#         clear_all,
#         outputs=[user_input, crop_name_input, crop_name_input, crop_submit_btn, medicine_table]
#     )
    
#     # Allow Enter key to submit
#     user_input.submit(
#         update_interface,
#         inputs=[user_input],
#         outputs=[response_output, crop_name_input, crop_submit_btn, medicine_table]
#     )

# if __name__ == "__main__":
#     app.launch(
#         server_name="0.0.0.0",  # Make it accessible from other devices
#         server_port=7860,       # Default Gradio port
#         share=False,            # Set to True if you want a public link
#         debug=True              # Set to False in production
#     )





























# # app.py (Gradio version - keeping your existing logic intact)

# import gradio as gr
# from db.db_query import query_agri_data
# from agri_keywords import is_agri_related
# from llm_query import get_response_from_llm
# import pandas as pd

# def process_user_input(user_input, crop_name_input=""):
#     """Main function to process user input - contains your existing logic"""
    
#     if not user_input:
#         return "Please enter a question about crops.", "", None
    
#     # Your existing logic starts here
#     if not is_agri_related(user_input):
#         return "❌ This query doesn't seem related to agriculture.", "", None
    
#     llm_response = get_response_from_llm(user_input)
    
#     if llm_response["type"] == "non-agri":
#         return f"❌ {llm_response['message']}", "", None
    
#     elif llm_response["type"] == "agri-fallback":
#         response_text = "⚠️ Partial match: Disease identified, but crop name is missing.\n\n"
        
#         if "points" in llm_response:
#             response_text += "### Disease Information\n"
#             for i, point in enumerate(llm_response["points"], start=1):
#                 response_text += f"**{i}.** {point}\n"
        
#         response_text += "\n**Please specify the crop name below to get medicine info:**"
        
#         # Handle crop name input if provided
#         medicine_data = None
#         if crop_name_input:
#             from llm_query import recent_context
#             disease = recent_context.get("disease")
#             if disease:
#                 db_results = query_agri_data(crop_name_input, disease)
#                 if db_results:
#                     response_text += f"\n\n✅ Crop: {crop_name_input} / Disease: {disease}\n"
#                     response_text += "### Recommended Medicines:\n"
                    
#                     df = pd.DataFrame(db_results)
#                     medicine_data = df
#                 else:
#                     response_text += f"\n\n⚠️ No medicine found for {crop_name_input}-{disease} combination."
#             else:
#                 response_text += "\n\n❌ Something went wrong — disease context missing."
        
#         general_info = llm_response["message"]
#         if general_info and not general_info.strip().startswith("{"):
#             response_text += f"\n\n---\n#### Additional Info\n{general_info}"
        
#         return response_text, "", medicine_data
    
#     elif llm_response["type"] == "agri-general":
#         response_text = "✅ General Agriculture Question Detected\n\n### Information\n"
#         for i, point in enumerate(llm_response.get("points", []), start=1):
#             response_text += f"**{i}.** {point}\n"
        
#         return response_text, "", None
    
#     elif llm_response["type"] == "agri-match":
#         crop = llm_response.get("crop")
#         disease = llm_response.get("disease")
        
#         response_text = f"✅ Identified: {crop} / {disease}\n\n"
        
#         points = llm_response.get("points", [])
#         if isinstance(points, list) and points:
#             response_text += "### Disease Information\n"
#             for i, point in enumerate(points, start=1):
#                 response_text += f"**{i}.** {point}\n"
#         else:
#             response_text += "⚠️ Disease info not available in structured format.\n"
        
#         products = query_agri_data(crop=crop, disease=disease)
#         medicine_data = None
        
#         if products:
#             response_text += "\n### Recommended Medicines\n"
            
#             df = pd.DataFrame(products)
#             df = df[
#                 ["trade_name", "generic_name", "crop", "disease", "dose_per_acre",
#                  "company", "category", "price_pkr", "efficacy_test_result"]
#             ]
#             df.rename(columns={
#                 "trade_name": "Trade Name",
#                 "generic_name": "Generic Name",
#                 "crop": "Crop",
#                 "disease": "Disease",
#                 "dose_per_acre": "Dose per Acre",
#                 "company": "Company",
#                 "category": "Category",
#                 "price_pkr": "Price (PKR)",
#                 "efficacy_test_result": "Efficacy"
#             }, inplace=True)
            
#             def format_price(x):
#                 try:
#                     return f"PKR {int(x):,}"
#                 except:
#                     return str(x)
            
#             df["Price (PKR)"] = df["Price (PKR)"].apply(format_price)
#             medicine_data = df
#         else:
#             response_text += "\n⚠️ No medicines found for this crop-disease combination."
        
#         return response_text, "", medicine_data
    
#     return "Something went wrong. Please try again.", "", None

# def handle_crop_name_submission(user_input, crop_name):
#     """Handle when user submits crop name for fallback case"""
#     return process_user_input(user_input, crop_name)

# # Create Gradio Interface
# with gr.Blocks(title="Agri Crop Advisor", theme=gr.themes.Soft()) as app:
#     gr.Markdown("# 🌾 Agri Crop Solution Assistant")
#     gr.Markdown("Ask about crop issues in English or Roman Urdu")
    
#     with gr.Row():
#         with gr.Column(scale=2):
#             user_input = gr.Textbox(
#                 label="Your Question",
#                 placeholder="Ask about a crop issue (English, Roman Urdu)...",
#                 lines=2
#             )
            
#             with gr.Row():
#                 submit_btn = gr.Button("Submit Question", variant="primary")
#                 clear_btn = gr.Button("Clear", variant="secondary")
            
#             # Crop name input (for fallback cases)
#             crop_name_input = gr.Textbox(
#                 label="Crop Name (if requested above)",
#                 placeholder="Enter crop name...",
#                 visible=False
#             )
#             crop_submit_btn = gr.Button("Submit Crop Name", visible=False, variant="primary")
    
#     with gr.Row():
#         with gr.Column():
#             response_output = gr.Markdown(label="Response")
            
#             # Medicine data table (conditionally shown)
#             medicine_table = gr.Dataframe(
#                 label="Recommended Medicines",
#                 visible=False,
#                 interactive=False
#             )

#     def update_interface(user_input, crop_name=""):
#         response, _, medicine_data = process_user_input(user_input, crop_name)
        
#         # Check if we need crop name input (fallback case)
#         show_crop_input = "Please specify the crop name below" in response
#         show_medicine_table = medicine_data is not None
        
#         return (
#             response,
#             gr.update(visible=show_crop_input),
#             gr.update(visible=show_crop_input),
#             gr.update(value=medicine_data, visible=show_medicine_table)
#         )
    
#     def clear_all():
#         return "", "", gr.update(visible=False), gr.update(visible=False), gr.update(visible=False, value=None)
    
#     # Event handlers
#     submit_btn.click(
#         update_interface,
#         inputs=[user_input],
#         outputs=[response_output, crop_name_input, crop_submit_btn, medicine_table]
#     )
    
#     crop_submit_btn.click(
#         update_interface,
#         inputs=[user_input, crop_name_input],
#         outputs=[response_output, crop_name_input, crop_submit_btn, medicine_table]
#     )
    
#     clear_btn.click(
#         clear_all,
#         outputs=[user_input, crop_name_input, crop_name_input, crop_submit_btn, medicine_table]
#     )
    
#     # Allow Enter key to submit
#     user_input.submit(
#         update_interface,
#         inputs=[user_input],
#         outputs=[response_output, crop_name_input, crop_submit_btn, medicine_table]
#     )

# if __name__ == "__main__":
#     app.launch(
#         server_name="0.0.0.0",  # Make it accessible from other devices
#         server_port=7860,       # Default Gradio port
#         share=False,            # Set to True if you want a public link
#         debug=True              # Set to False in production
#     )







































































# # # app.py (main entry point for Streamlit app)


# import streamlit as st
# from db.db_query import query_agri_data
# from agri_keywords import is_agri_related
# from llm_query import get_response_from_llm
# import pandas as pd

# st.set_page_config(page_title="Agri Crop Advisor")
# st.title(" Agri Crop Solution Assistant")

# user_input = st.text_input("Ask about a crop issue (English, Roman Urdu):")

# if user_input:
#     if not is_agri_related(user_input):
#         st.error(" This query doesn't seem related to agriculture.")
#     else:
#         llm_response = get_response_from_llm(user_input)

#         if llm_response["type"] == "non-agri":
#             st.error(llm_response["message"])

#         elif llm_response["type"] == "agri-fallback":
#             st.warning(" Partial match: Disease identified, but crop name is missing.")

#             if "points" in llm_response:
#                 st.markdown("### Disease Information")
#                 for i, point in enumerate(llm_response["points"], start=1):
#                     st.markdown(f"**{i}.** {point}")

#             st.markdown(" Please specify the crop name to get medicine info:")
#             crop_name = st.text_input("Enter crop name:", key="ask_crop")

#             if crop_name:
#                 from llm_query import recent_context
#                 disease = recent_context.get("disease")
#                 if disease:
#                     db_results = query_agri_data(crop_name, disease)
#                     if db_results:
#                         st.success(f" Crop: {crop_name} / Disease: {disease}")
#                         st.markdown("### Recommended Medicines:")
#                         df = pd.DataFrame(db_results)
#                         st.dataframe(df)
#                     else:
#                         st.warning(" No medicine found for this crop-disease combination.")
#                 else:
#                     st.error("Something went wrong — disease context missing.")

#             general_info = llm_response["message"]

#             # Show additional explanation only if it's not a raw JSON object
#             if general_info and not general_info.strip().startswith("{"):
#                 st.markdown("---")
#                 st.markdown("#### Additional Info")
#                 st.markdown(general_info)

#         elif llm_response["type"] == "agri-general":
#             st.success("General Agriculture Question Detected")
#             st.markdown("### Information")
#             for i, point in enumerate(llm_response.get("points", []), start=1):
#                 st.markdown(f"**{i}.** {point}")

#             # st.markdown(llm_response.get("message", ""))

#         elif llm_response["type"] == "agri-match":
#             crop = llm_response.get("crop")
#             disease = llm_response.get("disease")

#             st.success(f" Identified: {crop} / {disease}")

#             points = llm_response.get("points", [])
#             if isinstance(points, list) and points:
#                 st.markdown("### Disease Information")
#                 for i, point in enumerate(points, start=1):
#                     st.markdown(f"**{i}.** {point}")
#             else:
#                 st.warning(" Disease info not available in structured format.")

#             products = query_agri_data(crop=crop, disease=disease)
#             if products:
#                 st.markdown("### Recommended Medicines")

#                 df = pd.DataFrame(products)
#                 df = df[
#                     ["trade_name", "generic_name", "crop", "disease", "dose_per_acre",
#                      "company", "category", "price_pkr", "efficacy_test_result"]
#                 ]
#                 df.rename(columns={
#                     "trade_name": "Trade Name",
#                     "generic_name": "Generic Name",
#                     "crop": "Crop",
#                     "disease": "Disease",
#                     "dose_per_acre": "Dose per Acre",
#                     "company": "Company",
#                     "category": "Category",
#                     "price_pkr": "Price (PKR)",
#                     "efficacy_test_result": "Efficacy"
#                 }, inplace=True)

#                 def format_price(x):
#                     try:
#                         return f"PKR {int(x):,}"
#                     except:
#                         return str(x)

#                 df["Price (PKR)"] = df["Price (PKR)"].apply(format_price)
#                 st.dataframe(df, use_container_width=True)
#             else:
#                 st.warning(" No medicines found for this crop-disease combination.")
