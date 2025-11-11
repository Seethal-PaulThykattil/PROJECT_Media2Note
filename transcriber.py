# backend/transcriber.py
import assemblyai as aai
import os
from dotenv import load_dotenv

load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def transcribe_audio(audio_file):
    """
    Transcribes a lecture audio file and returns the text.
    """
    if not aai.settings.api_key:
        raise ValueError("❌ Missing AssemblyAI API key in .env file")

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)

    if transcript and transcript.text:
        print("✅ Transcription complete.")
        return transcript.text
    else:
        print("⚠️ No transcription output found.")
        return ""
