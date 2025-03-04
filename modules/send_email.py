import pyautogui
import time
import webbrowser
from modules.speech import SpeechHandler
import os 
class SendEmail:
    def __init__(self, speech_handler: SpeechHandler):
        self.speech_handler = speech_handler

    def open_gmail(self):
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
        self.speech_handler.speak("Opening Gmail. Please wait...")
        time.sleep(3)  # Ajuste si nécessaire

    def click_new_message(self):
        self.speech_handler.speak("Clicking on 'New Message'.")
        time.sleep(3)  # Wait for Gmail to load

        try:
            img_path = "img/new_message.png"
            if not os.path.exists(img_path):
                self.speech_handler.speak("Error: 'New Message' button image not found.")
                return False  # Stop execution
            
            button_location = pyautogui.locateCenterOnScreen(img_path, confidence=0.7)
            if button_location:
                pyautogui.click(button_location)
                self.speech_handler.speak("New message window opened.")
                return True  # Continue process
            else:
                self.speech_handler.speak("Could not find 'New Message'. Try clicking manually.")
                return False  # Stop execution

        except Exception as e:
            self.speech_handler.speak(f"Error clicking 'New Message': {e}")
            return False  # Stop execution

    async def get_voice_input(self, prompt, retries=2):
   
        for attempt in range(retries):
            self.speech_handler.speak(prompt)
            time.sleep(1)

            try:
                response = await self.speech_handler.listen_command()
                if response:
                    return response.strip().lower()
            except Exception as e:
                self.speech_handler.speak(f"Error processing speech: {e}")
        
        self.speech_handler.speak("I didn't hear you. Let's try again.")
        return ""


    async def type_recipient(self):
        recipient = await self.get_voice_input("Who do you want to send the email to?")   
        if recipient:
            pyautogui.write(recipient + "@gmail.com")
            pyautogui.press("tab")
            self.speech_handler.speak(f"Recipient set to {recipient}.")
            time.sleep(1)

    async def type_subject(self):
        subject = await self.get_voice_input("What is the subject of your email?") 
        if subject:
            pyautogui.write(subject)
            pyautogui.press("tab")
            self.speech_handler.speak(f"Subject set to {subject}.")
            time.sleep(1)

    async def type_message(self):
        message = await self.get_voice_input("What is the message?") 
        if message:
            pyautogui.write(message)
            self.speech_handler.speak("Message written")
            time.sleep(1)
        
    async def handle_attachments(self):
        """Handles file attachment process"""
        try:
            self.speech_handler.speak("Looking for attach button.")   
            attach_btn = pyautogui.locateCenterOnScreen("img/files.png")
            if attach_btn:
                pyautogui.click(attach_btn)
                self.speech_handler.speak("Please select your file in the dialog. I'll wait 20 seconds.")
                time.sleep(20)  # Wait for user to select file
                self.speech_handler.speak("File attached successfully.")
            else:
                self.speech_handler.speak("Could not find attach button. Please attach manually.")
        except Exception as e:
            self.speech_handler.speak(f"Attachment error: {e}")



    async def ask_attachments(self):
        response = await self.get_voice_input("Do you want to attach any files or images? Say yes or no.")
        
        if response in ["yes", "yeah", "sure", "okay", "alright"]:
            await self.handle_attachments()
        elif response in ["no", "nah", "skip"]:
            self.speech_handler.speak("Skipping attachments.")
        else:
            self.speech_handler.speak("I didn't understand. Please say yes or no.")
            await self.ask_attachments()  # Ask again
  
  
  
    async def send_email(self):
        confirmation = await self.get_voice_input("Say 'yes' to send the email or 'no' to cancel.")
        if "yes" in confirmation.lower():
            pyautogui.hotkey("ctrl", "enter")
            self.speech_handler.speak("Email sent successfully.")

    async def handle_send_email(self):
        self.open_gmail()
        
        success = self.click_new_message()
        if not success:
            self.speech_handler.speak("Email process cancelled because 'New Message' could not be found.")
            return  

        await self.type_recipient()
        await self.type_subject()
        await self.type_message()
        await self.ask_attachments()
        await self.send_email()