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
