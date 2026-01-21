import argparse
import sys
import multiprocessing

import os

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    os.environ['DEEPFACE_HOME'] = base_path
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

sys.path.append(".")

def main():
    multiprocessing.freeze_support()
    parser = argparse.ArgumentParser(description="DeepFace Access Control Application")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--ManageUsers', action='store_true', help='Open directly to the Dashboard')
    group.add_argument('--FaceRecognition', action='store_true', help='Open directly to the Face Recognition page')
    group.add_argument('--HiddenCam', action='store_true', help='Run the background service (hidden camera)')
    parser.add_argument('--timeout', type=int, help='Timeout in seconds to automatically close the application', default=None)
    
    args = parser.parse_args()

    if args.HiddenCam:
        print("Starting Background Service (HiddenCam)...")
        from background_service import main as run_service
        run_service(timeout=args.timeout)
        
    elif args.ManageUsers:
        print("Starting Application (ManageUsers)...")
        from main import run_app
        run_app(start_mode='dashboard')
        
    elif args.FaceRecognition:
        print("Starting Application (FaceRecognition)...")
        from main import run_app
        run_app(start_mode='recognition')
        
    else:
        print("Starting Application (Default)...")
        from main import run_app
        run_app(start_mode='default')

if __name__ == '__main__':
    main()
