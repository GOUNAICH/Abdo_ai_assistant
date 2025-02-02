import requests
import json
import os
from modules.speech import SpeechHandler
from dotenv import load_dotenv

load_dotenv()

speech_handler = SpeechHandler()

def chatBot(query):

    MODEL = "mistralai/Mistral-Nemo-Instruct-2407"
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

    HF_TOKEN = os.getenv("HF_TOKEN")
    if not HF_TOKEN:
        raise ValueError("HuggingFace token not found in .env file")

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }


    payload = {
        "inputs": query,
        "parameters": {
            "max_new_tokens": 100
        }
    }

    try:
        # Send the API request
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status() 

        # Parse the response
        result = response.json()[0]['generated_text']

        # Clean up the response
        if result.startswith(query):
            result = result[len(query):].strip() 


        result = result.split(result)[0].strip() if result.count(result) > 1 else result

        result = result.replace("?", "").strip()  # Remove "?"
        result = result.replace("\n", " ").strip()  # Remove newlines
        result = result.replace("</think>", "").strip()  # Remove </think> if present

        speech_handler.speak(result)

        return result

    except requests.exceptions.RequestException as e:
        
        print(f"API Request Error: {e}")
        speech_handler.speak("Sorry, there was an error processing your request.")
        return "Sorry, there was an error processing your request."
    
    

#  def chatBot(query):
#    user_input = query.lower()
#    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
#    id = chatbot.new_conversation()
#    chatbot.change_conversation(id)
#    response =  chatbot.chat(user_input)
#    print(response)
#    speech_handler.speak(response)
#    return response