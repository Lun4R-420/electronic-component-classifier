from ultralytics import YOLO
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MODEL_PATH = PROJECT_ROOT / "runs" / "detect" / "train" / "weights" / "best.onnx"

def load_model():
    return YOLO(MODEL_PATH)

def run_detection(model, source):
    result = model.predict(source=source)
    detections = []
    for box in result[0].boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        confidence = round(float(box.conf[0]), 2)
        x1, y1, x2, y2 = map(float, box.xyxyn[0])
        detections.append({
            "class_name": class_name,
            "confidence": confidence,
            "bounding_box": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
        })
    return detections