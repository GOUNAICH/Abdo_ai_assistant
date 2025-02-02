import sys
import asyncio
from PyQt6.QtWidgets import QApplication
import qasync
from GraphiqueInterface.MainWindow import MainWindow
from assistant import AIAssistant

async def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    loop = qasync.QEventLoop(app)

                
    asyncio.set_event_loop(loop)

    assistant = AIAssistant(window)
    assistant.speech_handler.speak("Hello, How can I assist you today?")

    try:
        while True:
            command = await assistant.speech_handler.listen_command()
            if command:
                await assistant.execute_command_async(command)
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await loop.create_task(app.exec())

if __name__ == "__main__":
    asyncio.run(main())