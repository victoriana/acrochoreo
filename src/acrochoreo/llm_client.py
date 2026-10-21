import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Walk up from this file: gemini_client.py -> agentic_eval_harness -> src -> repo root
ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

def ask_ai(question: str) -> str:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=question,
    )
    return response.text.strip()