🧠 Gemini Python Expert Chatbot with Guardrails (Chainlit + OpenAI SDK)
This project is an AI-powered Python expert chatbot built using:

🧠 Chainlit for the chat interface

🔒 Input guardrails to filter out non-Python queries

🚀 OpenAI SDK (compatible with Gemini API)

✅ Pydantic for schema validation

🔑 API integration via .env

🚀 Features
✅ Only answers Python-related questions

🔍 Guardrail agent checks each question before it reaches the expert agent

💬 Built using Chainlit for a clean chat UI

🌐 Uses Gemini API (Google) through OpenAI-compatible SDK

⚙️ Fully async and scalable with Runner.run pattern

📁 File Structure

├── main.py              # Main chatbot logic with Chainlit events
├── .env                 # Your Gemini API key
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

🔧 Setup Instructions
Clone this repo
git clone https://github.com/your-username/python-gemini-guardrails-chatbot.git
cd python-gemini-guardrails-chatbot

Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

Install dependencies
pip install -r requirements.txt

Create a .env file
GEMINI_API_KEY=your_google_gemini_api_key_here

Run the app
chainlit run main.py

🧪 Example Prompts
✅ Allowed:

"How do I use list comprehension in Python?"
"What is the difference between @staticmethod and @classmethod?"

❌ Blocked:

"Tell me a joke."
"What is the capital of France?"

📜 License
This project is open-sourced under the MIT License.
