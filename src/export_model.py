from ultralytics import YOLO
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MODEL_PATH = PROJECT_ROOT / "runs" / "detect" / "train" / "weights" / "best.pt"

model = YOLO(MODEL_PATH)
model.export(format="onnx", dynamic=True, opset=17, simplify=True, device="cpu")