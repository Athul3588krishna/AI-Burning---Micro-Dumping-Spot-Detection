import argparse
import os
import sys
from app.detector import WasteDetector
from app.config import OUTPUT_IMAGE_DIR, OUTPUT_VIDEO_DIR, MODEL_PATH

def main():
    parser = argparse.ArgumentParser(description="AI Burning & Micro-Dumping Spot Detection CLI")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--image", type=str, help="Path to input image file")
    group.add_argument("--video", type=str, help="Path to input video file")
    
    parser.add_argument("--cooldown", type=float, default=30.0, help="Cooldown period in seconds for video logging (default: 30.0)")
    parser.add_argument("--conf", type=float, default=0.5, help="Confidence threshold for YOLO (default: 0.5)")
    parser.add_argument("--model", type=str, default=MODEL_PATH, help="Path to custom model weights")

    args = parser.parse_args()

    # Initialize the detector
    detector = WasteDetector(
        model_path=args.model,
        confidence_threshold=args.conf
    )

    if args.image:
        if not os.path.exists(args.image):
            print(f"Error: Image file not found at {args.image}")
            sys.exit(1)
            
        print(f"Processing image: {args.image}...")
        filename = os.path.basename(args.image)
        output_path = os.path.join(OUTPUT_IMAGE_DIR, f"annotated_{filename}")
        
        detections = detector.detect_image(args.image, output_path)
        
        print(f"\nProcessing complete! Annotated image saved to: {output_path}")
        print(f"Total detections: {len(detections)}")
        for idx, det in enumerate(detections, 1):
            print(f"  {idx}. {det['class']} (Conf: {det['confidence']:.2f})")

    elif args.video:
        if not os.path.exists(args.video):
            print(f"Error: Video file not found at {args.video}")
            sys.exit(1)
            
        print(f"Processing video: {args.video}...")
        filename = os.path.basename(args.video)
        output_path = os.path.join(OUTPUT_VIDEO_DIR, f"annotated_{filename}")
        
        # Simple progress printer
        def print_progress(progress):
            percent = progress * 100
            sys.stdout.write(f"\rProgress: {percent:.1f}%")
            sys.stdout.flush()

        violations_logged = detector.detect_video(
            video_path=args.video,
            output_path=output_path,
            cooldown_seconds=args.cooldown,
            progress_callback=print_progress
        )
        
        print(f"\n\nProcessing complete! Annotated video saved to: {output_path}")
        print(f"Total violations logged to database: {violations_logged}")

if __name__ == "__main__":
    main()
