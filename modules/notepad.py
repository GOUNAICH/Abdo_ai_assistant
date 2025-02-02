import subprocess
import time
import pyautogui
import win32clipboard
from win32con import CF_UNICODETEXT

class NotepadHandler:
    def __init__(self, speech_handler):
        self.speech_handler = speech_handler
        self.current_notepad = None
        self.is_dictating = False
        self.max_save_attempts = 3

    async def start_notepad_dictation(self):
        try:
            self.current_notepad = subprocess.Popen(['notepad.exe'])
            time.sleep(1)
            self.is_dictating = True
            self.speech_handler.speak("Notepad is open. What would you like me to write?")
        except Exception as e:
            print(f"Error opening Notepad: {e}")
            self.speech_handler.speak("Sorry, I couldn't open Notepad.")

    async def write_to_notepad(self, text):
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(CF_UNICODETEXT, text)
            win32clipboard.CloseClipboard()
            pyautogui.hotkey('ctrl', 'v')
            self.speech_handler.speak("Text written. Continue or say 'save file'.")
        except Exception as e:
            print(f"Error writing to Notepad: {e}")
            self.speech_handler.speak("Sorry, I couldn't write the text.")

    async def save_notepad_file(self):
        attempts = 0
        while attempts < self.max_save_attempts:
            try:
                self.speech_handler.speak("Please say the filename you want to use.")
                filename = await self.speech_handler.listen_command()
                
                if not filename:
                    attempts += 1
                    if attempts < self.max_save_attempts:
                        self.speech_handler.speak("I didn't catch that. Please try again.")
                        continue
                    else:
                        self.speech_handler.speak("I'm having trouble understanding the filename. Let's use a default name.")
                        filename = f"note_{time.strftime('%Y%m%d_%H%M%S')}"
                
                filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_'))
                
                pyautogui.hotkey('ctrl', 's')
                time.sleep(1)
                pyautogui.write(f"{filename}.txt")
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)
                
                self.is_dictating = False
                self.current_notepad = None
                self.speech_handler.speak(f"File saved as {filename}.txt.")
                return
                
            except Exception as e:
                print(f"Error saving file (attempt {attempts + 1}): {e}")
                attempts += 1
                if attempts < self.max_save_attempts:
                    self.speech_handler.speak("Sorry, there was an error saving. Let's try again.")
                else:
                    self.speech_handler.speak("I'm having trouble saving the file. Please try manually saving it.")

    async def add_space(self):
        """Add a space in the Notepad."""
        try:
            pyautogui.press('space')
            self.speech_handler.speak("Space added.")
        except Exception as e:
            print(f"Error adding space: {e}")
            self.speech_handler.speak("Sorry, I couldn't add a space.")

    async def add_new_line(self):
        """Add a new line in the Notepad."""
        try:
            pyautogui.press('enter')
            self.speech_handler.speak("New line added.")
        except Exception as e:
            print(f"Error adding new line: {e}")
            self.speech_handler.speak("Sorry, I couldn't add a new line.")

    async def add_tab(self):
        """Add a tab in the Notepad."""
        try:
            pyautogui.press('tab')
            self.speech_handler.speak("Tab added.")
        except Exception as e:
            print(f"Error adding tab: {e}")
            self.speech_handler.speak("Sorry, I couldn't add a tab.")

    async def delete_last_character(self):
        """Delete the last character in the Notepad."""
        try:
            pyautogui.press('backspace')
            self.speech_handler.speak("Last character deleted.")
        except Exception as e:
            print(f"Error deleting character: {e}")
            self.speech_handler.speak("Sorry, I couldn't delete the character.")

    async def clear_notepad(self):
        """Clear all text in the Notepad."""
        try:
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.5)
            pyautogui.press('delete')
            self.speech_handler.speak("Notepad cleared.")
        except Exception as e:
            print(f"Error clearing Notepad: {e}")
            self.speech_handler.speak("Sorry, I couldn't clear the text.")
            
    async def go_back(self):
        """go back."""
        try:
            pyautogui.hotkey('ctrl', 'z')
            self.speech_handler.speak("go back added.")
        except Exception as e:
            print(f"Error adding tab: {e}")
            self.speech_handler.speak("Sorry, I couldn't add a tab.")
    
    async def go_next(self):
        """go_next."""
        try:
            pyautogui.hotkey('ctrl', 'y')
            self.speech_handler.speak("go_next added.")
        except Exception as e:
            print(f"Error adding tab: {e}")
            self.speech_handler.speak("Sorry, I couldn't add a tab.")
