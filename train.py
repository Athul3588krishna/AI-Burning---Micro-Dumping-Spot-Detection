import argparse
import os
import shutil
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser(description="Train YOLOv11 on Custom Dataset")
    parser.add_argument("--model", type=str, default="yolo11n.pt", help="Path to pre-trained model (default: yolo11n.pt)")
    parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs (default: 50)")
    parser.add_argument("--batch", type=int, default=16, help="Batch size (default: 16)")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size (default: 640)")
    parser.add_argument("--device", type=str, default="", help="Device to run on, e.g., 0 or cpu")
    parser.add_argument("--workers", type=int, default=8, help="Number of data loading workers (default: 8)")
    
    args = parser.parse_args()
    
    # Path to dataset configuration
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_yaml_path = os.path.join(base_dir, "dataset", "data.yaml")
    
    if not os.path.exists(data_yaml_path):
        print(f"Error: Dataset configuration file not found at {data_yaml_path}")
        return

    print(f"Loading model: {args.model}")
    model = YOLO(args.model)
    
    print(f"Starting training on {data_yaml_path}...")
    print(f"Parameters: Epochs={args.epochs}, Batch size={args.batch}, Image size={args.imgsz}")
    
    # Run training
    model.train(
        data=data_yaml_path,
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device if args.device else None,
        workers=args.workers,
        project="runs/detect",
        name="train_yolo11",
        exist_ok=True
    )
    
    print("Training completed!")
    
    # Copy best weights to the models directory
    best_weights_path = os.path.join("runs", "detect", "train_yolo11", "weights", "best.pt")
    if os.path.exists(best_weights_path):
        dest_dir = os.path.join(base_dir, "models")
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, "best.pt")
        shutil.copy(best_weights_path, dest_path)
        print(f"Saved best model weights to: {dest_path}")
    else:
        print("Warning: Could not find trained weights at runs/detect/train_yolo11/weights/best.pt")

if __name__ == "__main__":
    main()
