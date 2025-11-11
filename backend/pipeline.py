import os
from cnn_detect import detect_teachers
from cnn_ocr_extract import extract_text_from_images as extract_text_from_frames

from transcriber import transcribe_audio
from summarizer import summarize_text

def process_pipeline(video_file_path):
    print("🚀 Starting Media2Note Pipeline...")

    if not os.path.exists(video_file_path):
        return "❌ File not found."

    print("[1/4] Detecting frames with CNN...")
    detect_teachers(video_file_path)

    print("[2/4] Extracting text from frames...")
    lecture_text = extract_text_from_frames("detected_frames")

    print("[3/4] Transcribing audio...")
    audio_file = "lecture_audio.mp3"
    transcript_text = ""
    if os.path.exists(audio_file):
        transcript_text = transcribe_audio(audio_file)
    else:
        print("⚠️ No audio file found, skipping transcription.")

    print("[4/4] Summarizing...")
    combined_text = lecture_text + "\n" + transcript_text
    summary = summarize_text(combined_text)

    with open("final_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("✅ Process complete! Summary saved to final_summary.txt")
    return summary
