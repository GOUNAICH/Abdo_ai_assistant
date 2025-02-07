import sys
import requests
import os
from PyQt6.QtWidgets import QApplication, QFileDialog
from dotenv import load_dotenv
from modules.speech import SpeechHandler

# Load API token
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HuggingFace token not found in .env file")

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

class ImageCaptioning:
    def __init__(self, speech_handler):
        self.speech_handler = speech_handler

    def query(self, filename):
        try:
            with open(filename, "rb") as f:
                data = f.read()
            response = requests.post(API_URL, headers=headers, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def describe_image(self):
        self.speech_handler.speak("Please select an image.")
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Select an Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"
        )

        if file_path:
            self.speech_handler.speak("Processing the image. Please wait.")
            output = self.query(file_path)
            if "error" in output:
                self.speech_handler.speak("Sorry, there was an error processing the image.")
            else:
                description = output[0]['generated_text'] if output else "No description available."
                self.speech_handler.speak(f"Here is the description: {description}")
        else:
            self.speech_handler.speak("No file selected.")