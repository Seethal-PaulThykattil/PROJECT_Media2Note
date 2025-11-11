import os
import glob
import cv2
import json
import argparse
import numpy as np
import pytesseract
from ultralytics import YOLO
from typing import Dict, Any, List
def extract_text_from_images(detection_results):
    # loop through results, perform OCR for each teacher box
    # return dictionary like { "image_name.jpg": { "teacher_boxes": [...], "extracted_text": "..." } }
    ...


# --- Configuration ---
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
MODEL_NAME = "yolov8n.pt"
DEFAULT_CONFIDENCE = 0.4
TARGET_CLASS = "person"

OUTPUT_JSON = "lecture_notes.json"
OUTPUT_TEXT = "full_lecture.txt"

# --- Functions ---
def setup_tesseract(path: str):
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        print("✅ Tesseract path set.")
    else:
        print(f"❌ Tesseract not found at {path}")

def preprocess_image_for_ocr(img: np.ndarray, teacher_boxes: List[List[float]]) -> np.ndarray:
    masked_img = img.copy()
    for x1, y1, x2, y2 in [map(int, box) for box in teacher_boxes]:
        masked_img[max(0, y1):min(img.shape[0], y2), max(0, x1):min(img.shape[1], x2)] = 255
    gray = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def process_frame(img_path: str, model: YOLO, conf_thres: float) -> Dict[str, Any]:
    results = model.predict(source=img_path, conf=conf_thres, device='cpu', verbose=False)
    teacher_boxes = []
    for r in results:
        if r.boxes:
            for box in r.boxes:
                cls = int(box.cls[0])
                class_name = model.names.get(cls, "Unknown")
                if class_name == TARGET_CLASS:
                    teacher_boxes.append(box.xyxy[0].tolist())

    img = cv2.imread(img_path)
    if img is None:
        return {"error": "Image load failed"}

    processed_img = preprocess_image_for_ocr(img, teacher_boxes)
    try:
        text = pytesseract.image_to_string(processed_img, config='--psm 6').strip()
    except Exception as e:
        text = f"OCR Error: {e}"

    return {
        "teacher_boxes": teacher_boxes,
        "extracted_text": text
    }

def run_extraction(frame_folder: str, conf_thres: float, output_json: str, output_text: str):
    setup_tesseract(TESSERACT_PATH)
    print(f"🔄 Loading YOLO model: {MODEL_NAME}...")
    model = YOLO(MODEL_NAME)

    frame_files = glob.glob(os.path.join(frame_folder, "*.*"))
    if not frame_files:
        print(f"⚠️ No frames found in {frame_folder}")
        return

    all_results = {}
    print(f"🎬 Processing {len(frame_files)} frames...")
    for i, img_path in enumerate(frame_files):
        filename = os.path.basename(img_path)
        print(f"[{i+1}/{len(frame_files)}] {filename}")
        all_results[filename] = process_frame(img_path, model, conf_thres)

    # Save JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
    print(f"✅ Extraction results saved to {output_json}")

    # Combine text from all frames
    full_text = ""
    for frame, content in sorted(all_results.items()):
        text = content.get("extracted_text", "")
        full_text += f"--- {frame} ---\n{text}\n\n"

    with open(output_text, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"✅ Full lecture text saved to {output_text}")

# --- Entry point ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLOv8 + OCR for lecture frames")
    parser.add_argument("-f", "--folder", type=str, default="uploads")
    parser.add_argument("-c", "--conf", type=float, default=DEFAULT_CONFIDENCE)
    parser.add_argument("-j", "--json", type=str, default=OUTPUT_JSON)
    parser.add_argument("-t", "--text", type=str, default=OUTPUT_TEXT)
    args = parser.parse_args()

    run_extraction(args.folder, args.conf, args.json, args.text)
