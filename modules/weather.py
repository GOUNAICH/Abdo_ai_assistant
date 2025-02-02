import requests
import asyncio

class WeatherHandler:
    def __init__(self, speech_handler, weather_api_key):
        self.speech_handler = speech_handler
        self.weather_api_key = weather_api_key

    async def get_weather_async(self):
        try:
            lat, lon = "30.239660", "-9.526830"
            url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.weather_api_key}'
            response = await asyncio.to_thread(requests.get, url)
            data = response.json()

            if response.status_code == 200:
                temp = data['main']['temp'] - 273.15
                weather = data['weather'][0]['description']
                self.speech_handler.speak(f"Current temperature is {temp:.1f}°C with {weather}")
            else:
                self.speech_handler.speak("Sorry, I couldn't fetch the weather information")

        except Exception as e:
            print(f"Weather error: {e}")
            self.speech_handler.speak("Sorry, there was an error getting the weather")