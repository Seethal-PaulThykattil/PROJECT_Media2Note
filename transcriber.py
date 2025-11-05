import subprocess
import assemblyai as aai
from transformers import T5ForConditionalGeneration, T5Tokenizer

# ============================================================
# 🔑 SETUP: Add your AssemblyAI API key directly here
# ============================================================
aai.settings.api_key = "6870d96822584a8ca384c1a5f18d4332"  # Replace with your own key

if not aai.settings.api_key:
    raise ValueError("❌ AssemblyAI API key not found. Please set it before running.")


# ============================================================
# 🎵 Step 1: Extract audio URL from YouTube
# ============================================================
def get_audio_url_from_youtube(youtube_url: str) -> str | None:
    """
    Uses yt-dlp to extract direct audio URL from a YouTube video.
    """
    try:
        print("🎬 Extracting audio URL from YouTube...")
        result = subprocess.run(
            ["yt-dlp", "-f", "bestaudio", "-g", youtube_url],
            capture_output=True,
            text=True,
            check=True,
        )
        audio_url = result.stdout.strip()
        print(f"✅ Extracted audio URL: {audio_url}")
        return audio_url
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error extracting audio URL: {e}")
        return None


# ============================================================
# 🗣️ Step 2: Transcribe the audio
# ============================================================
def transcribe_audio_from_url(audio_url: str) -> str | None:
    """
    Transcribes audio from a given URL using AssemblyAI.
    """
    if not audio_url:
        print("⚠️ No audio URL provided for transcription.")
        return None

    try:
        print("🎧 Starting transcription using AssemblyAI...")
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


# ============================================================
# 🧠 Step 3: Summarize the text
# ============================================================
def summarize_text(text: str) -> str:
    """
    Summarizes transcribed text using the T5 transformer model.
    """
    if not text:
        print("⚠️ No text to summarize.")
        return "No summary generated due to missing transcription."

    try:
        print("🧠 Summarizing text...")
        model = T5ForConditionalGeneration.from_pretrained("t5-base")
        tokenizer = T5Tokenizer.from_pretrained("t5-base")

        input_ids = tokenizer.encode(
            "summarize: " + text,
            return_tensors="pt",
            max_length=1024,
            truncation=True,
        )
        output = model.generate(
            input_ids, max_length=300, num_beams=4, early_stopping=True
        )
        summary = tokenizer.decode(output[0], skip_special_tokens=True)

        print("✅ Summary complete.")
        return summary
    except Exception as e:
        print(f"⚠️ Error during summarization: {e}")
        return "Summary generation failed."


# ============================================================
# 🚀 Step 4: Run standalone
# ============================================================
if __name__ == "__main__":
    youtube_url = input("🎥 Enter YouTube video URL: ").strip()
    if not youtube_url:
        print("⚠️ No URL entered. Exiting.")
        exit()

    audio_url = get_audio_url_from_youtube(youtube_url)
    if not audio_url:
        print("❌ Failed to extract audio. Exiting.")
        exit()

    text = transcribe_audio_from_url(audio_url)
    if not text:
        print("❌ Transcription failed. Exiting.")
        exit()

    print("\n📝 --- Full Transcription ---")
    print(text)

    summary = summarize_text(text)
    print("\n🧾 --- Summary ---")
    print(summary)
