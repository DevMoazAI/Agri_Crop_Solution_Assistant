
## 📸 Application Screenshots

### 🔹 English Query  
![Homepage](App_Images/screenshot_7.png)

### 🔹 English Description  
![Dashboard](App_Images/screenshot_8.png)

### 🔹 Medicien from Database  
![Form](App_Images/screenshot_9.png)

### 🔹 URDU Query and Description  
![Mobile View](App_Images/screenshot_11.png)

### 🔹 Medicien from Database  
![Mobile View](App_Images/screenshot_12.png)

![Homepage](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(7).png)
![Dashboard](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(8).png)
![Form](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(9).png)
![Mobile View](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(11).png)
![Mobile View 2](https://raw.githubusercontent.com/DevMoazAI/Agri_Crop_Solution_Assistant/main/App_Images/Screenshot%20(12).png)


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

Let me know if you’re deploying via Streamlit, Flask, or FastAPI — I can tweak this accordingly.
