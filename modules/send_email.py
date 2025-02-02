import pyautogui
import time
import webbrowser
from modules.speech import SpeechHandler

class SendEmail:
    def __init__(self, speech_handler: SpeechHandler):
        self.speech_handler = speech_handler

    def open_gmail(self):
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
        self.speech_handler.speak("Opening Gmail. Please wait...")
        time.sleep(1)  # Ajuste si nécessaire

    def click_new_message(self):
        """Clique sur 'New Message' via reconnaissance d'image."""
        self.speech_handler.speak("Clicking on 'New Message'.")
        time.sleep(1)

        try:
            button_location = pyautogui.locateCenterOnScreen("img/new_message_button.png")
            if button_location:
                pyautogui.click(button_location)
                self.speech_handler.speak("New message window opened.")
            else:
                self.speech_handler.speak("Could not find 'New Message'. Try clicking it manually.")
        except Exception as e:
            self.speech_handler.speak(f"Error clicking 'New Message': {e}")

    async def get_voice_input(self, prompt):
        """Gère la saisie vocale de manière asynchrone."""
        self.speech_handler.speak(prompt)
        time.sleep(1)

        try:
            response = await self.speech_handler.listen_command()   
            return response.strip() if response else ""
        except Exception as e:
            self.speech_handler.speak(f"Error processing speech: {e}")
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
            attach_btn = pyautogui.locateCenterOnScreen("img/attach_button.png")
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
        """Asks if user wants to add attachments"""
        response = await self.get_voice_input("Do you want to attach any files or images? Say yes or no.")
        if "yes" in response.lower():
            await self.handle_attachments()
        else:
            self.speech_handler.speak("Email not sent.")
            
    async def send_email(self):
        confirmation = await self.get_voice_input("Say 'yes' to send the email or 'no' to cancel.")
        if "yes" in confirmation.lower():
            pyautogui.hotkey("ctrl", "enter")
            self.speech_handler.speak("Email sent successfully.")

    async def handle_send_email(self):
        """Exécute le processus d'envoi d'email."""
        self.open_gmail()
        self.click_new_message()
        await self.type_recipient()
        await self.type_subject()
        await self.type_message()
        await self.ask_attachments()
        await self.send_email()
