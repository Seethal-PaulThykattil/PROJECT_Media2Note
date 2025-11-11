import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
def summarize_text(text):
    # use T5 or any summarization model
    # return summarized string
    ...


genai.configure(api_key=os.getenv("AIzaSyCg6ILZyw_c3-MdXa6LMls-LDBYDxPIK9M"))

def summarize_text(text):
    model = genai.GenerativeModel("models/gemini-2.5-flash-preview-09-2025")
    prompt = f"Summarize the following lecture text clearly and concisely:\n\n{text}"

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"
