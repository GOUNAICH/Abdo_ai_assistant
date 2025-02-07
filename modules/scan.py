import urllib.request as request
import numpy as np
import cv2
import time
import os
from PIL import Image
from modules.speech import SpeechHandler

class PhoneScreenCapture:
    def __init__(self, speech_handler):
        self.speech_handler = speech_handler
        self.url = 'http://192.168.43.1:8080/photoaf.jpg'  # IP Webcam image URL
        # Get documents folder path
        self.docs_folder = os.path.join(os.path.expanduser('~'), 'Documents', 'PhoneCaptures')
        # Create folder if it doesn't exist
        os.makedirs(self.docs_folder, exist_ok=True)
        self.captured_files = []  # Store paths of captured files

    def show_captured_files(self):
        """Display the last captured image and open the PDF"""
        if not self.captured_files:
            self.speech_handler.speak("No files were captured in this session.")
            return

        # Show the last captured image
        last_jpg = [f for f in self.captured_files if f.endswith('.jpg')]
        if last_jpg:
            img = cv2.imread(last_jpg[-1])
            if img is not None:
                cv2.imshow('Last Captured Image', img)
                cv2.waitKey(0)
                cv2.destroyWindow('Last Captured Image')

        # Try to open the PDF with default system viewer
        last_pdf = [f for f in self.captured_files if f.endswith('.pdf')]
        if last_pdf:
            try:
                os.startfile(last_pdf[-1])  # Windows
            except AttributeError:
                try:
                    import subprocess
                    if os.name == 'posix':  # macOS and Linux
                        subprocess.run(['open' if os.name == 'darwin' else 'xdg-open', last_pdf[-1]])
                except Exception as e:
                    print(f"Could not open PDF: {e}")

    def capture_screen(self):
        self.speech_handler.speak("Starting phone screen capture. Press 'S' to save or 'Q' to exit.")
        
        while True:
            try:
                img_resp = request.urlopen(self.url)
                img_np = np.asarray(bytearray(img_resp.read()), dtype=np.uint8)
                frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
                if frame is None:
                    print("Error: Cannot load image.")
                    self.speech_handler.speak("Error loading image from phone.")
                    continue
                
                cv2.namedWindow('Phone Screen Capture', cv2.WINDOW_GUI_NORMAL)
                cv2.imshow('Phone Screen Capture', frame)
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('s'):  # Save image
                    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
                    filename_jpg = os.path.join(self.docs_folder, f'{timestamp}.jpg')
                    filename_pdf = os.path.join(self.docs_folder, f'{timestamp}.pdf')
                    
                    # Save JPG
                    cv2.imwrite(filename_jpg, frame)
                    self.captured_files.append(filename_jpg)
                    
                    # Save PDF
                    Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).save(filename_pdf)
                    self.captured_files.append(filename_pdf)
                    
                    print(f"Saved: {filename_jpg} & {filename_pdf}")
                    self.speech_handler.speak("Image captured and saved.")
                    
                elif key == ord('q'):  # Quit
                    self.speech_handler.speak("Exiting phone screen capture. If you want to see your latest images and PDFs, please check PhoneCaptures inside the Documents folder")                
                    break
                    
            except Exception as e:
                print(f"Error: {e}")
                self.speech_handler.speak("An error occurred while capturing the phone screen.")
                break
        
        cv2.destroyAllWindows()