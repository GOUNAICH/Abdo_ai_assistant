import sys
import asyncio
import random
import re
import PyPDF2
from PyQt6.QtWidgets import QApplication, QFileDialog
from modules.speech import SpeechHandler
import webbrowser
from modules.utils import find_application

class InteractivePDFCompanion:
    def __init__(self, file_path=None):
        self.speaker = SpeechHandler()
        self.file_path = file_path if file_path else self.select_pdf_file()
        self.pdf_reader = None
        self.total_pages = 0
        self.book = None
        self.current_page = 0
        self.current_paragraph = 0
        self.structure = []
        
        self.reactions = [
            "Ready for more?",
            "Shall we continue?",
            "Would you like to hear that again?",
            "What do you think so far?",
        ]

    def select_pdf_file(self):
        self.speaker.speak("Please select a PDF to read.")
        app = QApplication.instance() or QApplication(sys.argv)
        file_path, _ = QFileDialog.getOpenFileName(None, "Select a PDF file", "", "PDF Files (*.pdf)")
        
        if not file_path:
            self.speaker.speak("No file selected. Goodbye!")
            sys.exit()
        
        self.speaker.speak("Great choice!")
        return file_path

    def parse_page_structure(self, text):
        lines = text.split('\n')
        structure = []
        current_paragraph = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if len(line) < 100 and (line.isupper() or line.istitle()):
                if current_paragraph:
                    structure.append(('paragraph', ' '.join(current_paragraph)))
                    current_paragraph = []
                structure.append(('title', line))
            else:
                current_paragraph.append(line)
                
            if line.endswith('.'):
                if current_paragraph:
                    structure.append(('paragraph', ' '.join(current_paragraph)))
                    current_paragraph = []
                    
        if current_paragraph:
            structure.append(('paragraph', ' '.join(current_paragraph)))
        
        return structure

    def open_pdf(self):
        try:
            self.speaker.speak("Please wait a second to open the PDF.")
            chrome_path = find_application("chrome")  # Get Chrome's path dynamically

            if chrome_path:
                webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))
                webbrowser.get("chrome").open(self.file_path)
            else:
                self.speaker.speak("Google Chrome not found. Opening in the default browser instead.")
                webbrowser.open(self.file_path)

            # Load the PDF for reading
            self.book = open(self.file_path, "rb")
            self.pdf_reader = PyPDF2.PdfReader(self.book)
            self.total_pages = len(self.pdf_reader.pages)

            self.speaker.speak(f"PDF loaded. {self.total_pages} pages available.")
            return True

        except Exception as e:
            self.speaker.speak(f"Error opening PDF: {str(e)}")
            return False

    def load_page(self, page_num):
        self.current_page = page_num
        self.speaker.speak(f"Reading page {self.current_page + 1}")
        page = self.pdf_reader.pages[page_num]
        text = page.extract_text() or "No readable text on this page."
        self.structure = self.parse_page_structure(text)
        self.current_paragraph = 0
    
    async def ask_page_number(self):
        while True:
            self.speaker.speak("Which page do you want me to read?")
            response = await self.speaker.listen_command()
            
            if response and response.isdigit():
                page_num = int(response)
                if 1 <= page_num <= self.total_pages:
                    return page_num - 1
                else:
                    self.speaker.speak(f"Please choose between 1 and {self.total_pages}.")
            else:
                self.speaker.speak("Please say a number.")

    async def handle_command(self):
        self.speaker.speak("Say: 'continue', 'repeat', 'next page', 'previous page', 'go to page X' or 'stop'")
        command = await self.speaker.listen_command()
        
        if command:
            command = command.lower()
            if 'stop' in command:
                return False
            elif 'repeat' in command:
                return 'repeat'
            elif 'next page' in command:
                if self.current_page < self.total_pages - 1:
                    self.current_page += 1
                    self.load_page(self.current_page)
                    return 'next_page'
                else:
                    self.speaker.speak("This is the last page.")
                    return 'repeat'
            elif 'previous page' in command:
                if self.current_page > 0:
                    self.current_page -= 1
                    self.load_page(self.current_page)
                    return 'previous_page'
                else:
                    self.speaker.speak("This is the first page.")
                    return 'repeat'
            elif 'go to page' in command:
                match = re.search(r'go to page (\d+)', command)
                if match:
                    page_number = int(match.group(1)) - 1
                    if 0 <= page_number < self.total_pages:
                        self.current_page = page_number
                        self.load_page(self.current_page)
                        return 'go_to_page'
                    else:
                        self.speaker.speak(f"Invalid page number. Choose between 1 and {self.total_pages}.")
                        return 'repeat'
            elif 'continue' in command:
                if self.current_paragraph < len(self.structure) - 1:
                    self.current_paragraph += 1
                    return 'continue'
                else:
                    self.speaker.speak("End of page reached. Say 'next page', 'previous page' or 'go to page X'.")
                    return 'repeat'
        
        return 'repeat'
    
    async def read_current_section(self):
        if 0 <= self.current_paragraph < len(self.structure):
            section_type, content = self.structure[self.current_paragraph]
            
            if section_type == 'title':
                self.speaker.speak(f"Title: {content}")
            else:
                self.speaker.speak(f"Paragraph {self.current_paragraph + 1}: {content}")
            
            self.speaker.speak(random.choice(self.reactions))
    
    async def start_reading(self):
        if not self.open_pdf():  # Open in browser before asking for a page
            return
        
        await asyncio.sleep(2)  # Small delay to allow the PDF to load in the browser
        page_num = await self.ask_page_number()  # Ask user which page to read
        self.load_page(page_num)
        
        while True:
            await self.read_current_section()
            command = await self.handle_command()
            
            if command is False:
                self.speaker.speak("Thanks for reading! Goodbye!")
                break
            elif command == 'next_page':
                self.speaker.speak(f"Moving to page {self.current_page + 1}")
            elif command == 'previous_page':
                self.speaker.speak(f"Going back to page {self.current_page + 1}")
            elif command == 'go_to_page':
                self.speaker.speak(f"Jumping to page {self.current_page + 1}")
            elif command == 'repeat':
                continue
        
        self.book.close()

async def main():
    pdf_companion = InteractivePDFCompanion()
    await pdf_companion.start_reading()

if __name__ == "__main__":
    asyncio.run(main())
