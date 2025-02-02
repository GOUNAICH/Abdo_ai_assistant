from datetime import datetime
import random

class BasicCommands:
    def __init__(self, speech_handler):
        self.speech_handler = speech_handler

    async def execute_command(self, command):
        if 'what time is it' in command:
            current_time = datetime.now().strftime("%H:%M")
            self.speech_handler.speak(f"It's {current_time}")

        elif 'what is the date' in command:
            current_date = datetime.now().strftime("%B %d, %Y")
            self.speech_handler.speak(f"Today is {current_date}")

        elif 'tell me a joke' in command:
            self.tell_joke()

    def tell_joke(self):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the math book look sad? Because it had too many problems!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "What did the grape say when it got stepped on? Nothing, it just let out a little wine!"
        ]
        joke = random.choice(jokes)
        self.speech_handler.speak(joke)