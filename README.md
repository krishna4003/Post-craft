# Post-craft
Post Crafter – AI-Driven Social Media Content Generator Post Crafter is a FastAPI-based backend application that uses OpenAI's GPT-4 to generate compelling Instagram and Twitter posts for product marketing. Users can select platforms, choose content templates, generate engaging hooks, and craft the final social media post—all powered by AI.

Features
✅ Submit a product name for marketing

✅ Choose a target platform (Instagram or Twitter)

✅ Select from 5 different post templates

✅ Generate 5 AI-powered hook lines

✅ Choose a hook and get a tailored final post

✅ Uses OpenAI's GPT-4 via openai-python SDK

📦 Tech Stack
Backend: FastAPI

Language: Python

AI Model: OpenAI GPT-4

Web Server: Uvicorn

🔧 Installation
1.Clone the repository
git clone https://github.com/your-username/post-crafter.git
cd post-crafter
2.Set up a virtual environment
python -m venv env
source env/bin/activate   # or `env\Scripts\activate` on Windows
3.Install dependencies
pip install -r requirements.txt
4.Set OpenAI API Key
export OPENAI_API_KEY=your_key_here   # Linux/Mac
set OPENAI_API_KEY=your_key_here      # Windows
▶️ Run the app
uvicorn main:app --reload
The app will be available at: http://127.0.0.1:8000
