import argparse
from ultralytics import YOLO
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "ElectroCom61 A Multiclass Dataset for Detection of Electronic Components" / "ElectroCom-61_v2" / "data.yaml"

def parse_args():
    parser = argparse.ArgumentParser(description="Training script for the model.")
    parser.add_argument("--model", type=str, default="yolo11s.pt", help="Path to the model weights.")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs.")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size for training.")
    parser.add_argument("--patience", type=int, default=15, help="Early stopping patience.")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size for training.")
    parser.add_argument("--workers", type=int, default=0, help="Number of data loading workers.")

    return parser.parse_args()

def train():
    args = parse_args()
    model = YOLO(args.model)
    model.train(data=DATASET_PATH, 
                epochs=args.epochs, 
                imgsz=args.imgsz, 
                patience=args.patience, 
                batch=args.batch_size, 
                workers=args.workers,
                project=PROJECT_ROOT / "runs" / "train"
                )

if __name__ == "__main__":
    train()