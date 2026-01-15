import cv2
import time

def test_cam(index):
    print(f"Testing Camera Index {index}...")
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"FAILED: Could not open index {index}")
        return False
    
    ret, frame = cap.read()
    if ret:
        print(f"SUCCESS: Read frame from index {index} ({frame.shape})")
        cap.release()
        return True
    else:
        print(f"FAILED: Opened index {index} but could not read frame")
        cap.release()
        return False

print("--- Camera Diagnostic ---")
if test_cam(0):
    pass
else:
    test_cam(1)
print("-------------------------")
