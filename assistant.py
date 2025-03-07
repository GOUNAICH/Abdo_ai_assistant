from modules.speech import SpeechHandler
from modules.commands import BasicCommands
from modules.notepad import NotepadHandler
from modules.weather import WeatherHandler
from modules.ai_query import chatBot
from modules.phone_display import PhoneDisplayHandler
from modules.utils import find_application
from modules.img_generate import generate_img
from modules.send_email import SendEmail
from modules.volume_control import VolumeControl
import subprocess
import psutil
from dotenv import load_dotenv
import os
from auth import recoganize
from modules.img_to_text import ImageCaptioning
from modules.scan import PhoneScreenCapture
from modules.pdf_reader import InteractivePDFCompanion
from modules.about import Aboutcristiano

load_dotenv()

class AIAssistant:

    #flag = recoganize.AuthenticateFace()
    
    def __init__(self, window):
        self.window = window
        self.weather_api_key = os.getenv("WEATHER_API_KEY")
        self.cancel_flag = False
        # Initialize handlers
        self.speech_handler = SpeechHandler()
        self.basic_commands = BasicCommands(self.speech_handler)
        self.notepad_handler = NotepadHandler(self.speech_handler)
        self.weather_handler = WeatherHandler(self.speech_handler, self.weather_api_key)
        self.phone_display_handler = PhoneDisplayHandler(self.speech_handler)
        self.send_email_handler = SendEmail(self.speech_handler)
        self.volume_control = VolumeControl()
        self.image_captioning = ImageCaptioning(self.speech_handler)
        self.phone_screen_capture = PhoneScreenCapture(self.speech_handler)
        self.about_cristiano = Aboutcristiano(self.speech_handler)

        # Initialize PDF Reader
        self.pdf_reader = None

    async def execute_command_async(self, command):
        if not command:
            return

        print(f"User: {command}")

        try:
            
            if "cancel" in command or "stop" in command :
                self.cancel_flag=True
                self.speech_handler.stop_speaking()  # Stop ongoing speech
                self.speech_handler.speak("Cancelling teh current process...")
                
                if self.notepad_handler.is_dictating:
                    self.notepad_handler.is_dictating=False
                    subprocess.run(["taskkill", "/F", "/IM", "notepad.exe"], shell=True)
                    self.speech_handler.speak("Notepad Closed.")
                if self.pdf_reader and self.pdf_reader.is_reading:
                        self.pdf_reader.is_reading = False
                        subprocess.run(["taskkill", "/F", "/IM", "AcroRd32.exe"], shell=True)
                        self.speech_handler.speak("PDF reading cancelled.")

                    # Stop email sending if it was ongoing
                if hasattr(self.send_email_handler, "is_sending") and self.send_email_handler.is_sending:
                        self.send_email_handler.is_sending = False
                        self.speech_handler.speak("Email process cancelled.")
                
                return 
            elif "close" in command:
                    app_name = command.replace("close", "").strip().lower()
                    closed = self.close_application(app_name)
                    if closed:
                        self.speech_handler.speak(f"{app_name} closed successfully.")
                    else:
                        self.speech_handler.speak(f"Sorry, I couldn't find an application named {app_name} running.")

                    return  # Exit after closing app
                
            self.cancel_flag=False
              
            if "how are you" in command or "who built you" in command or "who created you" in command or "who made you" in command or "what can you do" in command or "your features" in command or "your capabilities" in command or "help me" in command or "thank you" in command or "thanks" in command:
                self.about_cristiano.respond(command)

            elif 'open notepad' in command:
                await self.notepad_handler.start_notepad_dictation()

            elif self.notepad_handler.is_dictating and any(word in command for word in ['save', 'save file', 'save it']):
                await self.notepad_handler.save_notepad_file()

            elif self.notepad_handler.is_dictating:
                
                while self.notepad_handler.is_dictating:
                    if self.cancel_flag:
                        self.speech_handler.speak("Dictation cancelled")
                        self.notepad_handler.is_dictating=False
                        return 
                # Handle special Notepad actions
                if 'add space' in command:
                    await self.notepad_handler.add_space()
                elif 'new line' in command or 'add line' in command:
                    await self.notepad_handler.add_new_line()
                elif 'add tab' in command or 'tab' in command:
                    await self.notepad_handler.add_tab()
                elif 'delete last character' in command or 'undo character' in command:
                    await self.notepad_handler.delete_last_character()
                elif 'clear notepad' in command or 'delete all' in command:
                    await self.notepad_handler.clear_notepad()
                elif 'go back' in command:
                    await self.notepad_handler.go_back()
                elif 'go next' in command:
                    await self.notepad_handler.go_next()
                else:
                    # Write regular text to Notepad
                    await self.notepad_handler.write_to_notepad(command)

            # Open applications
            elif 'open' in command:
                app_name = command.replace('open', '').strip().lower()
                app_path = find_application(app_name)
                if app_path:
                    subprocess.Popen([app_path])
                    self.speech_handler.speak(f"Opening {app_name}.")
                else:
                    self.speech_handler.speak(f"Sorry, I couldn't find an application named {app_name}.")

            # Web search
            elif "search for" in command:
                search_query = command.replace("search for", "").strip()
                if search_query:
                    subprocess.run(["start", f"https://www.google.com/search?q={search_query}"], shell=True)
                    self.speech_handler.speak(f"Searching for {search_query}.")
                else:
                    self.speech_handler.speak("Please specify what you'd like me to search for.")

            # Basic commands
            elif 'what time is it' in command or 'what is the date' in command or 'tell me a joke' in command:
                await self.basic_commands.execute_command(command)

            # Weather-related commands
            elif 'what\'s the weather' in command:
                await self.weather_handler.get_weather_async()

            # Phone display commands
            elif 'display my phone' in command:
                await self.phone_display_handler.display_phone()

            elif 'stop display' in command:
                self.phone_display_handler.stop_display()
                
                
            elif "generate image for" in command:
                filename = generate_img(command)
                if filename:
                    self.speech_handler.speak(f"Image generated and saved as {filename}.")
                else:
                    self.speech_handler.speak("Sorry, I couldn't generate the image.")
                    
            elif "send email" in command:
                await self.send_email_handler.handle_send_email()
            
            elif "volume up" in command or "increase volume" in command:
                self.volume_control.increase_volume()
                self.speech_handler.speak("Increasing volume.")

            elif "volume down" in command or "decrease volume" in command:
                self.volume_control.decrease_volume()
                self.speech_handler.speak("Decreasing volume.")

            elif "mute" in command:
                self.volume_control.mute_volume()
                self.speech_handler.speak("Volume muted.")

            elif "unmute" in command:
                self.volume_control.unmute_volume()
                self.speech_handler.speak("Volume unmuted.")

            elif "describe image" in command:
                self.image_captioning.describe_image()

            elif "scan document" in command:
                self.phone_screen_capture.capture_screen()

            elif "read pdf" in command:
                if not self.pdf_reader:
                    self.pdf_reader = InteractivePDFCompanion()
                    
                if self.cancel_flag: 
                    self.speech_handler.speak("PDF reading is cancelled")
                    self.pdf_reader.is_reading= False 
                    return 
                
                await self.pdf_reader.start_reading()

            # Default case: Pass any other command to the chatBot function
            else:
                chatBot(command)

        except Exception as e:
            print(f"Command execution error: {e}")
            self.speech_handler.speak("Sorry, there was an error executing that command.")
    
    def close_application(self, app_name):
            """Find and close a running application."""
            for process in psutil.process_iter(attrs=['pid', 'name']):
                if app_name.lower() in process.info['name'].lower():
                    try:
                        process.terminate()
                        return True
                    except Exception as e:
                        print(f"Error closing {app_name}: {e}")
                        return False
            return False