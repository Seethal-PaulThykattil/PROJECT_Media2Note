import os
import subprocess
import assemblyai as aai
from transformers import T5ForConditionalGeneration, T5Tokenizer


# === SETUP AssemblyAI API Key ===
# Prefer environment variable for local & server compatibility
# You can set this in your terminal before running the app:
#   setx ASSEMBLYAI_API_KEY "your_api_key_here"  (Windows)
#   export ASSEMBLYAI_API_KEY="your_api_key_here" (Mac/Linux)
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

if not aai.settings.api_key:
    raise ValueError("❌ AssemblyAI API key not found. Please set ASSEMBLYAI_API_KEY environment variable.")


# === Step 1: Extract audio from YouTube ===
def get_audio_url_from_youtube(youtube_url: str) -> str | None:
    """
    Uses yt-dlp to extract direct audio URL from a YouTube video.
    """
    try:
        result = subprocess.run(
            ['yt-dlp', '-f', 'bestaudio', '-g', youtube_url],
            capture_output=True,
            text=True,
            check=True
        )
        audio_url = result.stdout.strip()
        print(f"✅ Extracted audio URL: {audio_url}")
        return audio_url
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error extracting audio URL: {e}")
        return None


# === Step 2: Transcribe audio ===
def transcribe_audio_from_url(audio_url: str) -> str | None:
    """
    Transcribes audio from a given URL using AssemblyAI.
    """
    if not audio_url:
        print("⚠️ No audio URL provided for transcription.")
        return None

    try:
        print(f"🎧 Starting transcription from URL: {audio_url}")
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_url)
        if transcript.status == aai.TranscriptStatus.error:
            print(f"❌ Transcription failed: {transcript.error}")
            return None
        print("✅ Transcription complete.")
        return transcript.text
    except Exception as e:
        print(f"⚠️ Error during transcription: {e}")
        return None


# === Step 3: Summarize text using T5 ===
def summarize_text(text: str) -> str:
    """
    Summarizes transcribed text using the T5 transformer model.
    """
    if not text:
        print("⚠️ No text to summarize.")
        return "No summary generated due to missing transcription."

    try:
        print("🧠 Summarizing text...")
        model = T5ForConditionalGeneration.from_pretrained('t5-base')
        tokenizer = T5Tokenizer.from_pretrained('t5-base')
        input_ids = tokenizer.encode(
            "summarize: " + text,
            return_tensors='pt',
            max_length=1024,
            truncation=True
        )
        output = model.generate(
            input_ids,
            max_length=300,
            num_beams=4,
            early_stopping=True
        )
        summary = tokenizer.decode(output[0], skip_special_tokens=True)
        print("✅ Summary complete.")
        return summary
    except Exception as e:
        print(f"⚠️ Error during summarization: {e}")
        return "Summary generation failed."


# === Step 4: Optional standalone test ===
if __name__ == "__main__":
    youtube_url = input("Enter YouTube video URL: ").strip()
    audio_url = get_audio_url_from_youtube(youtube_url)
    if audio_url:
        text = transcribe_audio_from_url(audio_url)
        if text:
            print("\n--- Full Transcription ---")
            print(text)
            print("\n--- Summary ---")
            print(summarize_text(text))
        else:
            print("❌ Transcription failed.")
    else:
        print("❌ Failed to get audio URL from YouTube.")
