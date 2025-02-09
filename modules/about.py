import random
from modules.speech import SpeechHandler

class Aboutcristiano:
    def __init__(self, speech_handler):
        self.speech_handler = speech_handler
        self.greetings = [
            "How can I assist you today?",
            "Yep",
            "Ready to help!",
            "What can I do for you?",
            "I'm all ears!",
            "At your service!"
        ]
        
        self.features = {
            "document": "Document scanning",
            "phone": "Phone screen control",
            "image": "Image generation and analysis",
            "chat": "AI conversation",
            "email": "Email handling",
            "weather": "Weather updates",
            "notepad": "Voice-controlled text editing",
            "volume": "Volume control",
            "pdf": "PDF reading",
            "applications": "App launching and web search",
            "voice": "Voice command recognition"
        }
        
        self.thank_responses = [
            "You're welcome!",
            "No problem!",
            "Glad to help!",
            "Anytime!",
            "Happy to assist!"
        ]
        
    def respond(self, command):
        command = command.lower()
        
        if "cristiano" in command:
            response = random.choice(self.greetings)
            self.speech_handler.speak(response)
            
        elif "how are you" in command:
            responses = [
                "I'm functioning perfectly and ready to help!",
                "All systems operational and at your service!",
                "I'm doing great and excited to assist you!",
                "Running smoothly and ready for your commands!"
            ]
            self.speech_handler.speak(random.choice(responses))
            
        elif "who built you" in command or "who created you" in command or "who made you" in command:
            self.speech_handler.speak(
                "I was developed by Abdeslam Gounaich and Abdelhamid Ben Drif as an advanced virtual assistant."
            )
            
        elif "what can you do" in command or "your features" in command or "your capabilities" in command:
            self.speech_handler.speak(
                "I'm a versatile virtual assistant. Here are all my features:"
            )
            
            # List all features
            for feature in self.features.values():
                self.speech_handler.speak(feature)
                
            self.speech_handler.speak(
                "Would you like to know more about any specific feature?"
            )
                    
        elif "help me" in command:
            self.speech_handler.speak(
                "You can ask me to perform any task by using natural voice commands."
            )
            
        elif "thank you" in command or "thanks" in command:
            self.speech_handler.speak(random.choice(self.thank_responses))
            
        else:
            self.speech_handler.speak(
                "I didn't quite catch that. Feel free to ask about my features or give me a specific command."
            )