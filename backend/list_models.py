import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyCg6ILZyw_c3-MdXa6LMls-LDBYDxPIK9M"))

print("Available models:")
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print("-", m.name)
