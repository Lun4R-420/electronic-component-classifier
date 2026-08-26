import argparse
from inference import load_model, run_detection

def parse_args():
    parser = argparse.ArgumentParser(description="Run inference on a single image.")
    parser.add_argument("--image", type=str, required=True, help="Path to the input image.")
    return parser.parse_args()

def predict():
    args = parse_args()
    model = load_model()
    detections = run_detection(model, args.image)
    for d in detections:
        print(f"Detected: {d['class_name']}, Confidence: {d['confidence']}")
    return detections

if __name__ == "__main__":
    predict()