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
        os.makedirs(self.docs_folder, exist_ok=True)
        self.captured_files = []  # Store paths of captured files

    def detect_document(self, frame):
        """Detects the document in the image and applies perspective transformation."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        doc_contour = None
        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if len(approx) == 4:
                doc_contour = approx
                break

        if doc_contour is None:
            return frame  # No document found, return the original image

        # Order points for perspective transform
        def order_points(pts):
            rect = np.zeros((4, 2), dtype="float32")
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]
            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]
            return rect

        # Get a top-down perspective
        doc_contour = doc_contour.reshape(4, 2)
        rect = order_points(doc_contour)
        (tl, tr, br, bl) = rect

        width = max(int(np.linalg.norm(br - bl)), int(np.linalg.norm(tr - tl)))
        height = max(int(np.linalg.norm(tr - br)), int(np.linalg.norm(tl - bl)))

        dst = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]
        ], dtype="float32")

        matrix = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(frame, matrix, (width, height))

        return warped

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
                
                # Resize the frame to a smaller size
                frame_resized = cv2.resize(frame, (640, 480))
                cv2.imshow('Phone Screen Capture', frame_resized)
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('s'):  # Save image
                    document = self.detect_document(frame)  # Apply document detection

                    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
                    filename_jpg = os.path.join(self.docs_folder, f'{timestamp}.jpg')
                    filename_pdf = os.path.join(self.docs_folder, f'{timestamp}.pdf')
                    
                    # Save JPG
                    cv2.imwrite(filename_jpg, document)
                    self.captured_files.append(filename_jpg)
                    
                    # Save PDF
                    Image.fromarray(cv2.cvtColor(document, cv2.COLOR_BGR2RGB)).save(filename_pdf)
                    self.captured_files.append(filename_pdf)
                    
                    print(f"Saved: {filename_jpg} & {filename_pdf}")
                    self.speech_handler.speak("Document captured and saved.")
                    
                elif key == ord('q'):  # Quit
                    self.speech_handler.speak("Exiting phone screen capture. If you want to see your latest images and PDFs, please check PhoneCaptures inside the Documents folder")                
                    break
                    
            except Exception as e:
                print(f"Error: {e}")
                self.speech_handler.speak("An error occurred while capturing the phone screen.")
                break
        
        cv2.destroyAllWindows()
