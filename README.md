# 🌾 Agri Crop Solution Assistant

An AI-powered chatbot designed to assist farmers in **identifying crop diseases** and providing **accurate, contextual guidance**. This assistant understands user queries in both **Roman Urdu and English**, even handling common spelling mistakes and slang for seamless interaction.

---

## 📸 Application Screenshots

### 🔹 English Query
![English Query](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(7).png)

### 🔹 English Description
![English Description](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(8).png)

### 🔹 Medicine from Database (English)
![Medicine from Database (English)](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(9).png)

### 🔹 Urdu Query and Description
![Urdu Query and Description](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(11).png)

### 🔹 Medicine from Database (Urdu) - Example 1
![Medicine from Database (Urdu) - Example 1](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(12).png)

### 🔹 Medicine from Database (Urdu) - Example 2
![Medicine from Database (Urdu) - Example 2](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(14).png)

---

## 🚀 Key Features

* **🔍 Crop & Disease Detection**: Understands crop and disease names in both English and Roman Urdu.
* **🧠 LLM-Powered Query Understanding**: Leverages a Language Model to interpret user queries, including common spelling errors and slang.
* **🌐 Roman Urdu ↔ English Auto Response**: Intelligently replies in the same language as the user's initial question.
* **📌 Structured JSON Output**: Processes queries to return structured data, facilitating easy parsing and backend integration.
* **⚙️ Rule-Based Keyword Matching**: Employs local, rule-based keyword matching alongside flexible prompt engineering for efficient processing, minimizing external dependencies.

---

## 🧰 Tech Stack

* **Python 3.10+**
* **Gradio**: For building the interactive web user interface.
* **LangChain / LLM API**: (Configurable) for advanced language understanding.
* **JSON-based Keyword Matching**: For efficient data retrieval and processing.

---

## 🧠 How It Works

1.  **User Input**: The system accepts queries in either **Roman Urdu or English**.
2.  **Intelligent Parsing**: It detects relevant **crop and disease names** by leveraging custom keyword lists.
3.  **Fuzzy Matching**: Applies **fuzzy logic and an LLM** to robustly handle spelling mistakes and typos, ensuring high accuracy.
4.  **Structured Output**: If the query is agriculture-related, it returns a structured JSON output like this:
    ```json
    {
      "crop": "gandum",
      "disease": "leaf rust",
      "is_agriculture": true,
      "points": [ ... ],
      "products": []
    }
    ```
5.  **Contextual Reply**: The chatbot automatically replies in Roman Urdu or English, matching the language of the user's original query.

### 💬 Example Queries

| User Query                       | Response Language |
| :------------------------------- | :---------------- |
| `gadum ky paty peely ho rhy hain` | Roman Urdu        |
| `Leaves of wheat are turning yellow` | English           |
| `kapas ka pest ataak hai`        | Roman Urdu        |

---

## ⚙️ Setup and Run Locally

Follow these steps to get the Agri Crop Solution Assistant running on your local machine:

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/DevMoazAI/Agri_Crop_Solution_Assistant.git](https://github.com/DevMoazAI/Agri_Crop_Solution_Assistant.git)
    cd Agri_Crop_Solution_Assistant
    ```

2.  **Create a Virtual Environment**:
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment**:
    * **Windows**:
        ```bash
        venv\Scripts\activate
        ```
    * **Linux/macOS**:
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies**:
    Make sure you have a `requirements.txt` file in your project with all necessary libraries (e.g., `gradio`, `pandas`, `langchain`, etc.).
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Application**:
    This will launch the Gradio interface, typically accessible via your web browser at `http://127.0.0.1:5050` or `http://127.0.0.1:7860`.
    ```bash
    python gradio_ui.py
    ```
    *(Note: If port 5050 is in use, Gradio might automatically pick another port like 7860, or you can specify it in `app.launch()` in `gradio_ui.py`.)*

---

## 🙏 Credits

Built with 💚 by **Moaz Ahmad Khalid**

Supervised by **Solutyics AI Team**

---

## 📄 License

This project is open-source and available under the **MIT License**. Feel free to use, modify, and distribute it.















<!-- 
## 📸 Application Screenshots

### 🔹 English Query
![Homepage](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(7).png)

### 🔹 English Description 
![Dashboard](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(8).png)

### 🔹 Medicien from Database
![Form](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(9).png)

### 🔹 URDU Query and Description
![View](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(11).png)

### 🔹 Medicien from Database 
![View 2](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(12).png)

### 🔹 Medicien from Database 
![View 2](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(14).png)

# 🌾 Agri Crop Solution Assistant

An AI-powered Roman Urdu & English chatbot that helps farmers identify crop diseases and provides accurate, contextual guidance based on user queries — even with spelling mistakes!

---

## 🚀 Features

- 🔍 **Crop & Disease Detection** (English & Roman Urdu)
- 🤖 **LLM-Powered Query Understanding** (handles spelling errors and slang)
- 🌐 **Roman Urdu ↔ English Auto Response**: Replies in the same language as the user's question
- 📌 **Structured JSON Output**: For easy parsing & frontend use
- 🧠 **No External Dependencies**: Local rule-based keyword matching with flexible prompt engineering

---

## 🧰 Tech Stack

- Python 3.10+
- LangChain / LLM API (configurable)
- JSON-based Keyword Matching
- Streamlit / FastAPI (for deployment)

---

## 🧠 How It Works

1. Accepts user queries in **Roman Urdu or English**
2. Detects relevant **crop and disease names** from custom keyword lists
3. Applies **fuzzy logic and LLM** to understand spelling mistakes and typos
4. If agri-related, returns structured JSON:
   ```json
   {
     "crop": "gandum",
     "disease": "leaf rust",
     "is_agriculture": true,
     "points": [ ... ],
     "products": []
   }

Automatically replies in Roman Urdu or English, based on the query language

💬 Example Queries
User Query	Response Language
gadum ky paty peely ho rhy hain	Roman Urdu
Leaves of wheat are turning yellow	English
kapas ka pest ataak hai	Roman Urdu

🧪 To Run
git clone https://github.com/DevMoazAI/Agri_Crop_Solution_Assistant.git
cd Agri_Crop_Solution_Assistant
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate (Linux/macOS)
pip install -r requirements.txt
python app.py
🙏 Credits
Built with 💚 by Moaz Ahmad Khalid
Supervised by Solutyics AI Team

📄 License
MIT License – free to use, modify, and distribute.

---

Let me know if you’re deploying via Streamlit, Flask, or FastAPI — I can tweak this accordingly. -->
