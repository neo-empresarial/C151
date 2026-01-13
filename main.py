import sys
import argparse
from src.gui.recognition_ui import run_recognition
from src.gui.management_ui import run_management
from src.gui.main_window import run_launcher

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DeepFace Recognition App")
    parser.add_argument("--mode", choices=["recognition", "manage"], help="Mode to run the application in")
    
    args = parser.parse_args()
    
    if args.mode == "recognition":
        run_recognition()
    elif args.mode == "manage":
        run_management()
    else:
        run_launcher()
