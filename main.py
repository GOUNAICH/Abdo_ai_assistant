import asyncio
import sys
from assistant import AIAssistant

async def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'electron':
        print("Running with Electron integration", flush=True)
        input_signal = sys.stdin.readline().strip()
        print(f"Received input signal: {input_signal}", flush=True)

        if input_signal == 'window_ready':
            print("Initializing AI Assistant...", flush=True)
            assistant = AIAssistant(window='main_window_placeholder')

            # Initial greeting
            greeting = "Hello, How can I assist you today?"
            assistant.speech_handler.speak(greeting)  # This will print the greeting to stdout

            try:
                while True:
                    # Listen for a command
                    command = await assistant.speech_handler.listen_command()
                    if command:
                        await assistant.execute_command_async(command)
                        
                        

            except Exception as e:
                print(f"An error occurred: {e}", flush=True)

    else:
        print("Running standalone without Electron. Assistant will not have a window reference.", flush=True)

if __name__ == "__main__":
    asyncio.run(main())