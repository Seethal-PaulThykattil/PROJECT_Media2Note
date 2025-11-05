<<<<<<< HEAD:cnn_detect.py
import os
import subprocess
import assemblyai as aai
from transformers import T5ForConditionalGeneration, T5Tokenizer

# ==========================================================
# 🔑 1. Set your AssemblyAI API key directly here
# ==========================================================
aai.settings.api_key = "6870d96822584a8ca384c1a5f18d4332"

if not aai.settings.api_key:
    raise ValueError("❌ AssemblyAI API key not found. Please set it before running.")


# ==========================================================
# 🎵 2. Extract audio URL from a YouTube video
# ==========================================================
def get_audio_url_from_youtube(youtube_url: str) -> str:
    """Extract the direct audio URL from a YouTube video using yt-dlp."""
    try:
        print("🎧 Extracting audio URL from YouTube...")
        result = subprocess.run(
            ["yt-dlp", "-f", "bestaudio", "-g", youtube_url],
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


# ==========================================================
# 🗣️ 3. Transcribe audio directly from URL using AssemblyAI
# ==========================================================
def transcribe_audio_from_url(audio_url: str) -> str:
    """Transcribe audio from a given URL using AssemblyAI."""
    if not audio_url:
        print("⚠️ No audio URL provided for transcription.")
        return None

    try:
        print("📝 Starting transcription...")
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_url)

        if transcript.status == aai.TranscriptStatus.error:
            print(f"❌ Transcription error: {transcript.error}")
            return None

        print("✅ Transcription complete.")
        return transcript.text

    except Exception as e:
        print(f"⚠️ Error during transcription: {e}")
        return None


# ==========================================================
# ✂️ 4. Summarize transcribed text using a T5 model
# ==========================================================
def summarize_text(text: str) -> str:
    """
    Summarizes transcribed text using the T5 transformer model.
    Handles long text safely by chunking it.
    """
    if not text:
        print("⚠️ No text to summarize.")
        return "No summary generated due to missing transcription."

    try:
        print("🧠 Summarizing text...")
        model = T5ForConditionalGeneration.from_pretrained("t5-small")
        tokenizer = T5Tokenizer.from_pretrained("t5-small")

        # Split text into manageable chunks
        max_chunk_size = 500
        sentences = text.split(". ")
        chunks, chunk = [], ""

        for sentence in sentences:
            if len(chunk) + len(sentence) < max_chunk_size:
                chunk += sentence + ". "
            else:
                chunks.append(chunk.strip())
                chunk = sentence + ". "
        if chunk:
            chunks.append(chunk.strip())

        summaries = []
        for i, chunk in enumerate(chunks):
            print(f"🧩 Summarizing chunk {i + 1}/{len(chunks)}...")
            input_ids = tokenizer.encode(
                "summarize: " + chunk,
                return_tensors="pt",
                max_length=512,
                truncation=True,
            )
            output = model.generate(
                input_ids, max_length=120, num_beams=4, early_stopping=True
            )
            summary_part = tokenizer.decode(output[0], skip_special_tokens=True)
            summaries.append(summary_part)

        full_summary = " ".join(summaries)
        print("✅ Summary complete.")
        return full_summary

    except Exception as e:
        print(f"⚠️ Error during summarization: {e}")
        return "Summary generation failed."


# ==========================================================
# 🚀 5. Main function for CLI testing
# ==========================================================
def main():
    youtube_url = input("🔗 Enter YouTube video URL: ").strip()
    if not youtube_url:
        print("⚠️ No YouTube URL provided. Exiting.")
        return

    # Step 1: Extract audio URL
    audio_url = get_audio_url_from_youtube(youtube_url)
    if not audio_url:
        print("❌ Failed to get audio URL from YouTube.")
        return

    # Step 2: Transcribe the audio
    text = transcribe_audio_from_url(audio_url)
    if not text:
        print("❌ Transcription failed. Cannot proceed with summarization.")
        return

    # Step 3: Print full transcription
    print("\n📝 --- Full Transcription ---")
    print(text)

    # Step 4: Generate and print summary
    summary = summarize_text(text)
    print("\n🧾 --- Summary ---")
    print(summary)


# ==========================================================
# 🔥 Run Script
# ==========================================================
if __name__ == "__main__":
    main()
=======
# cnn_detect.py
# Detects person (teacher) in lecture frames using YOLOv8
# Saves output frames with bounding boxes and detection metadata

import os
import glob
import json
import cv2
import argparse
from ultralytics import YOLO

# ----------------------------
# Configuration
# ----------------------------
MODEL_NAME = "yolov8n.pt"  # lightweight YOLO model
CONF_THRESHOLD = 0.4
TARGET_CLASS = "person"
OUTPUT_JSON = "cnn_detection_results.json"
OUTPUT_FOLDER = "detected_frames"

# ----------------------------
# Core Logic
# ----------------------------
def run_detection(input_folder, conf_thres, output_json):
    print(f"🔄 Loading YOLO model: {MODEL_NAME} ...")
    model = YOLO(MODEL_NAME)

    frame_files = glob.glob(os.path.join(input_folder, "*.*"))
    if not frame_files:
        print(f"⚠️ No image frames found in {input_folder}")
        return

    # Create output folder if it doesn't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    all_results = {}

    print(f"🎬 Starting detection on {len(frame_files)} frames...\n")

    for i, img_path in enumerate(frame_files):
        filename = os.path.basename(img_path)
        print(f"[{i+1}/{len(frame_files)}] Processing: {filename}")

        # Run YOLO prediction
        results = model.predict(
            source=img_path,
            conf=conf_thres,
            device='cpu',
            verbose=False
        )

        frame_data = []
        img = cv2.imread(img_path)

        # Draw boxes
        for r in results:
            if r.boxes:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = model.names.get(cls, "Unknown")

                    if class_name == TARGET_CLASS:
                        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                        frame_data.append({
                            "class": class_name,
                            "confidence": conf,
                            "box": [x1, y1, x2, y2]
                        })
                        # Draw bounding box
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(img, f"{class_name} {conf:.2f}", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save annotated frame
        save_path = os.path.join(OUTPUT_FOLDER, filename)
        cv2.imwrite(save_path, img)

        # Store metadata
        all_results[filename] = frame_data

    # Save detection info to JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4)

    print(f"\n✅ Detection completed. Results saved to: {output_json}")
    print(f"✅ Annotated frames saved in: {OUTPUT_FOLDER}/")


# ----------------------------
# Entry Point
# ----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLOv8-based CNN Detection Script")
    parser.add_argument("-f", "--folder", type=str, default="uploads",
                        help="Folder containing lecture frames (default: uploads/)")
    parser.add_argument("-c", "--conf", type=float, default=CONF_THRESHOLD,
                        help="Confidence threshold (default: 0.4)")
    parser.add_argument("-o", "--output", type=str, default=OUTPUT_JSON,
                        help="Output JSON file for results (default: cnn_detection_results.json)")
    args = parser.parse_args()

    run_detection(args.folder, args.conf, args.output)
>>>>>>> 1afc19bf4d7cb340b0c57877aee9535b244f18df:backend/cnn_detect.py
