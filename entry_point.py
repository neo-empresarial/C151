import argparse
import sys
import multiprocessing

import os

if getattr(sys, 'frozen', False):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(sys.executable))
    
    # Deepface expects the home dir to contain .deepface folder
    # We copied .deepface to the root of the dist folder
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
    parser.add_argument('--CheckAccess', action='store_true', help='Run in access check mode (output via terminal)')
    parser.add_argument('--CloseAfter', action='store_true', help='Close application after successful access check')
    parser.add_argument('--timeout', type=int, help='Timeout in seconds to automatically close the application', default=None)
    
    args = parser.parse_args()



    if args.CheckAccess:
        import ctypes
        import sys
        import os
        
        ATTACH_PARENT_PROCESS = -1
        if ctypes.windll.kernel32.AttachConsole(ATTACH_PARENT_PROCESS):
            sys.stdout = open('CONOUT$', 'w')
            sys.stderr = open('CONOUT$', 'w')
        
        import logging
        logging.disable(logging.CRITICAL)
        import warnings
        warnings.filterwarnings('ignore')
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

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
        run_app(start_mode='recognition', timeout=args.timeout)
        
    elif args.CheckAccess:
        print("Starting Application (CheckAccess)...")
        from main import run_app
        run_app(start_mode='recognition', check_access=True, close_after=args.CloseAfter, timeout=args.timeout)
        
    else:
        print("Starting Application (Default)...")
        from main import run_app
        run_app(start_mode='default', check_access=args.CheckAccess, close_after=args.CloseAfter, timeout=args.timeout)

if __name__ == '__main__':
    main()
