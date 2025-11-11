import os
import json
from cnn_detect import detect_teachers
from cnn_ocr_extract import extract_text_from_images
from transcriber import transcribe_audio
from summarizer import summarize_text


def main():
    print("🚀 Starting full lecture processing pipeline...")

    # Step 1: Run teacher detection
    print("\n[1/4] Running CNN teacher detection...")
    detection_results = detect_teachers("input_images/")
    with open("cnn_detection_results.json", "w") as f:
        json.dump(detection_results, f, indent=4)

    # Step 2: Run OCR extraction
    print("\n[2/4] Extracting text from detected teacher boxes...")
    lecture_notes = extract_text_from_images(detection_results)
    with open("lecture_notes.json", "w") as f:
        json.dump(lecture_notes, f, indent=4)

    # Step 3: Run audio transcription
    print("\n[3/4] Transcribing audio...")
    audio_path = "lecture_audio.mp3"

    if not os.path.exists(audio_path):
        print(f"⚠️ Audio file '{audio_path}' not found. Skipping transcription.")
        transcript = ""
    else:
        transcript = transcribe_audio(audio_path)

    with open("full_lecture.txt", "w", encoding="utf-8") as f:
        f.write(transcript if transcript else "")

    # Step 4: Summarize the notes
    print("\n[4/4] Summarizing extracted content...")
    combined_text = (transcript or "") + "\n" + json.dumps(lecture_notes, indent=2)
    summary = summarize_text(combined_text)

    print("\n✅ Final Summary:\n")
    print(summary)

    # Save the summarized output
    with open("final_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print(
        "\n🎯 Pipeline complete! Files saved:\n"
        "- cnn_detection_results.json\n"
        "- lecture_notes.json\n"
        "- full_lecture.txt\n"
        "- final_summary.txt"
    )


if __name__ == "__main__":
    main()
