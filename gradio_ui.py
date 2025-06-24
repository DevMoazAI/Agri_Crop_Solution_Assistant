# gradio_ui.py
import gradio as gr
import re # Needed for the robust markdown bolding
from app_logic import process_user_input # Import your core logic

# Load custom CSS from the file
with open("style.css", "r") as f:
    custom_css = f.read()

# --- ADD THIS LINE HERE ---
# Font Awesome Local Hosting Link
# This line tells Gradio to load the Font Awesome CSS file from your 'static' folder.
# Make sure 'static/css/all.min.css' is the correct path to the Font Awesome CSS file
# you copied from the downloaded package. Use forward slashes (/) for paths.
font_awesome_link = '<link rel="stylesheet" href="/file=static/css/all.min.css">'
# --- END OF ADDITION ---

def format_response_with_styling(response_text):
    """Add CSS classes to status messages and convert markdown to HTML for professional styling."""

    # Apply styling to status messages
    if response_text.startswith("ERROR:"):
        response_text = f'<div class="status-error">{response_text}</div>'
    elif response_text.startswith("WARNING:"):
        response_text = f'<div class="status-warning">{response_text}</div>'
    elif response_text.startswith("SUCCESS:"):
        response_text = f'<div class="status-success">{response_text}</div>'

    # Convert markdown-style text to HTML
    # Use regex for robust bolding
    response_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', response_text)
    response_text = response_text.replace("### ", "<h3>").replace("#### ", "<h4>") # Add H4 as well
    response_text = response_text.replace("\n", "<br>")

    return response_text

def update_interface(user_input):
    """Handles the initial user query and updates the UI."""
    response, show_crop_input_flag, medicine_data = process_user_input(user_input)

    # Apply professional styling to response
    styled_response = format_response_with_styling(response)

    show_medicine_table = medicine_data is not None

    return (
        styled_response,
        gr.update(visible=show_crop_input_flag), # Show/hide crop input box
        gr.update(visible=show_crop_input_flag), # Show/hide crop submit button
        gr.update(value=medicine_data, visible=show_medicine_table) # Update and show/hide table
    )

def update_interface_with_crop(user_input_placeholder, crop_name_input_value):
    """Handles the submission of the crop name in fallback cases."""
    # Use the original user input for context (if needed by process_user_input)
    # Note: user_input_placeholder is the text from the main user_input box
    response, _, medicine_data = process_user_input(user_input_placeholder, crop_name_input_value)

    # Apply professional styling to response
    styled_response = format_response_with_styling(response)

    show_medicine_table = medicine_data is not None

    return (
        styled_response,
        gr.update(visible=False, value=""),  # Hide and clear crop input box
        gr.update(visible=False),            # Hide crop submit button
        gr.update(value=medicine_data, visible=show_medicine_table) # Update and show/hide table
    )

def clear_all():
    """Clears all UI elements."""
    return (
        "",  # user_input
        "",  # response_output (clear text)
        gr.update(visible=False, value=""),  # crop_name_input (hide and clear value)
        gr.update(visible=False),             # crop_submit_btn (hide)
        gr.update(visible=False, value=None)  # medicine_table (hide and clear value)
    )

# Create Gradio Interface
# --- MODIFY THIS LINE ---
# Now, the 'head' argument is added to gr.Blocks(), linking your Font Awesome CSS.
with gr.Blocks(title="Agri Crop Advisor", css=custom_css, theme=gr.themes.Base(), head=font_awesome_link) as app:
# --- END OF MODIFICATION ---
    gr.HTML('<div class="main-header"><h1>Agri Crop Solution Assistant</h1><p>Professional crop disease diagnosis and treatment recommendations</p></div>')

    with gr.Row(elem_classes=["main-content"]):
        with gr.Column(scale=1, elem_classes=["input-section"]):
            user_input = gr.Textbox(
                label="Your Question :fa-solid fa-question-circle:", # Added icon
                placeholder="Ask about a crop issue (English, Roman Urdu)...",
                lines=4,
                elem_classes=["input-field"]
            )

            with gr.Row():
                submit_btn = gr.Button("Submit Question :fa-solid fa-leaf:", elem_classes=["primary-btn"]) # Added icon
                clear_btn = gr.Button("Clear :fa-solid fa-eraser:", elem_classes=["secondary-btn"]) # Added icon

            # Crop name input (for fallback cases)
            crop_name_input = gr.Textbox(
                label="Crop Name (if requested above) :fa-solid fa-seedling:", # Added icon
                placeholder="Enter crop name...",
                visible=False,
                elem_classes=["input-field"]
            )
            crop_submit_btn = gr.Button("Submit Crop Name :fa-solid fa-check:", visible=False, elem_classes=["primary-btn"]) # Added icon

        with gr.Column(scale=1, elem_classes=["response-section"]):
            # Changed label to use icon
            response_output = gr.HTML(label="Response :fa-solid fa-comment-dots:", elem_classes=["response-area"])

            # Medicine data table (conditionally shown)
            medicine_table = gr.Dataframe(
                label="Recommended Medicines :fa-solid fa-pills:", # Added icon
                visible=False,
                interactive=False,
                elem_classes=["dataframe-container"]
            )

    # Event handlers - INSIDE the Blocks context
    submit_btn.click(
        update_interface,
        inputs=[user_input],
        outputs=[response_output, crop_name_input, crop_submit_btn, medicine_table]
    )

    crop_submit_btn.click(
        update_interface_with_crop,
        inputs=[user_input, crop_name_input], # Pass user_input to retain its value for process_user_input
        outputs=[response_output, crop_name_input, crop_submit_btn, medicine_table]
    )

    clear_btn.click(
        clear_all,
        outputs=[user_input, response_output, crop_name_input, crop_submit_btn, medicine_table]
    )

    # Allow Enter key to submit
    user_input.submit(
        update_interface,
        inputs=[user_input],
        outputs=[response_output, crop_name_input, crop_submit_btn, medicine_table]
    )

if __name__ == "__main__":
    app.launch(
        server_name= "127.0.0.1",
        # server_name="0.0.0.0",   # Make it accessible from other devices
        server_port=5050,        # Default Gradio port
        share=False,             # Set to True if you want a public link
        debug=True               # Set to False in production
    )

























# # gradio_ui.py
# import gradio as gr
# import re # Needed for the robust markdown bolding
# from app_logic import process_user_input # Import your core logic

# # Load custom CSS from the file
# with open("style.css", "r") as f:
#     custom_css = f.read()

# def format_response_with_styling(response_text):
#     """Add CSS classes to status messages and convert markdown to HTML for professional styling."""

#     # Apply styling to status messages
#     if response_text.startswith("ERROR:"):
#         response_text = f'<div class="status-error">{response_text}</div>'
#     elif response_text.startswith("WARNING:"):
#         response_text = f'<div class="status-warning">{response_text}</div>'
#     elif response_text.startswith("SUCCESS:"):
#         response_text = f'<div class="status-success">{response_text}</div>'

#     # Convert markdown-style text to HTML
#     # Use regex for robust bolding
#     response_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', response_text)
#     response_text = response_text.replace("### ", "<h3>").replace("#### ", "<h4>") # Add H4 as well
#     response_text = response_text.replace("\n", "<br>")

#     return response_text

# def update_interface(user_input):
#     """Handles the initial user query and updates the UI."""
#     response, show_crop_input_flag, medicine_data = process_user_input(user_input)

#     # Apply professional styling to response
#     styled_response = format_response_with_styling(response)

#     show_medicine_table = medicine_data is not None

#     return (
#         styled_response,
#         gr.update(visible=show_crop_input_flag), # Show/hide crop input box
#         gr.update(visible=show_crop_input_flag), # Show/hide crop submit button
#         gr.update(value=medicine_data, visible=show_medicine_table) # Update and show/hide table
#     )

# def update_interface_with_crop(user_input_placeholder, crop_name_input_value):
#     """Handles the submission of the crop name in fallback cases."""
#     # Use the original user input for context (if needed by process_user_input)
#     # Note: user_input_placeholder is the text from the main user_input box
#     response, _, medicine_data = process_user_input(user_input_placeholder, crop_name_input_value)

#     # Apply professional styling to response
#     styled_response = format_response_with_styling(response)

#     show_medicine_table = medicine_data is not None

#     return (
#         styled_response,
#         gr.update(visible=False, value=""),  # Hide and clear crop input box
#         gr.update(visible=False),            # Hide crop submit button
#         gr.update(value=medicine_data, visible=show_medicine_table) # Update and show/hide table
#     )

# def clear_all():
#     """Clears all UI elements."""
#     return (
#         "",  # user_input
#         "",  # response_output (clear text)
#         gr.update(visible=False, value=""),  # crop_name_input (hide and clear value)
#         gr.update(visible=False),             # crop_submit_btn (hide)
#         gr.update(visible=False, value=None)  # medicine_table (hide and clear value)
#     )

# # Create Gradio Interface
# with gr.Blocks(title="Agri Crop Advisor", css=custom_css, theme=gr.themes.Base()) as app:
#     gr.HTML('<div class="main-header"><h1>Agri Crop Solution Assistant</h1><p>Professional crop disease diagnosis and treatment recommendations</p></div>')

#     with gr.Row(elem_classes=["main-content"]):
#         with gr.Column(scale=1, elem_classes=["input-section"]):
#             user_input = gr.Textbox(
#                 label="Your Question :fa-solid fa-question-circle:", # Added icon
#                 placeholder="Ask about a crop issue (English, Roman Urdu)...",
#                 lines=4,
#                 elem_classes=["input-field"]
#             )

#             with gr.Row():
#                 submit_btn = gr.Button("Submit Question :fa-solid fa-leaf:", elem_classes=["primary-btn"]) # Added icon
#                 clear_btn = gr.Button("Clear :fa-solid fa-eraser:", elem_classes=["secondary-btn"]) # Added icon

#             # Crop name input (for fallback cases)
#             crop_name_input = gr.Textbox(
#                 label="Crop Name (if requested above) :fa-solid fa-seedling:", # Added icon
#                 placeholder="Enter crop name...",
#                 visible=False,
#                 elem_classes=["input-field"]
#             )
#             crop_submit_btn = gr.Button("Submit Crop Name :fa-solid fa-check:", visible=False, elem_classes=["primary-btn"]) # Added icon

#         with gr.Column(scale=1, elem_classes=["response-section"]):
#             # Changed label to use icon
#             response_output = gr.HTML(label="Response :fa-solid fa-comment-dots:", elem_classes=["response-area"])

#             # Medicine data table (conditionally shown)
#             medicine_table = gr.Dataframe(
#                 label="Recommended Medicines :fa-solid fa-pills:", # Added icon
#                 visible=False,
#                 interactive=False,
#                 elem_classes=["dataframe-container"]
#             )

#     # Event handlers - INSIDE the Blocks context
#     submit_btn.click(
#         update_interface,
#         inputs=[user_input],
#         outputs=[response_output, crop_name_input, crop_submit_btn, medicine_table]
#     )

#     crop_submit_btn.click(
#         update_interface_with_crop,
#         inputs=[user_input, crop_name_input], # Pass user_input to retain its value for process_user_input
#         outputs=[response_output, crop_name_input, crop_submit_btn, medicine_table]
#     )

#     clear_btn.click(
#         clear_all,
#         outputs=[user_input, response_output, crop_name_input, crop_submit_btn, medicine_table]
#     )

#     # Allow Enter key to submit
#     user_input.submit(
#         update_interface,
#         inputs=[user_input],
#         outputs=[response_output, crop_name_input, crop_submit_btn, medicine_table]
#     )

# if __name__ == "__main__":
#     app.launch(
#         server_name= "127.0.0.1",
#         # server_name="0.0.0.0",  # Make it accessible from other devices
#         server_port=5050,       # Default Gradio port
#         share=False,            # Set to True if you want a public link
#         debug=True              # Set to False in production
#     )