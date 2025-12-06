import os
import google.genai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found.")
else:
    client = genai.Client(api_key=GOOGLE_API_KEY)
    try:
        pager = client.models.list()
        print("Available Models:")
        for model in pager:
            print(f"- {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")
