import subprocess

class PhoneDisplayHandler:
    def __init__(self, speech_handler):
        self.speech_handler = speech_handler
        self.scrcpy_process = None
        self.is_phone_displayed = False

    async def display_phone(self):
        if self.is_phone_displayed:
            self.speech_handler.speak("Your phone screen is already being displayed.")
            return

        try:
            self.scrcpy_process = subprocess.Popen(
                r"C:\Users\dell\Desktop\Abdo_ai_assistant\Display_Phone\scrcpy.exe",
                shell=True)
            self.speech_handler.speak("Displaying your phone screen.")
            self.is_phone_displayed = True
        except Exception as e:
            print(f"Error starting scrcpy: {e}")
            self.speech_handler.speak("Failed to display your phone screen.")

    def stop_display(self):
        try:
            if self.is_phone_displayed and self.scrcpy_process:
                subprocess.run(['taskkill', '/F', '/IM', 'scrcpy.exe'], 
                             shell=True, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE)
                self.scrcpy_process = None
                self.is_phone_displayed = False
                self.speech_handler.speak("Stopped displaying phone screen.")
            else:
                self.speech_handler.speak("Phone screen is not being displayed.")
        except Exception as e:
            print(f"Error stopping display: {e}")
            self.speech_handler.speak("Error occurred while trying to stop the display.")