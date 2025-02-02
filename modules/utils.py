import os
import shutil
from fuzzywuzzy import fuzz

def find_application(app_name):
    # Common aliases
    aliases = {
        'code blocks': 'codeblocks',
        'postman': 'postman.exe',
    }
    app_name = aliases.get(app_name, app_name)

    # Check if app exists in system PATH
    if shutil.which(app_name):
        return app_name

    # Search in common directories with fuzzy matching
    common_dirs = [
        r"C:\\Program Files",
        r"C:\\Program Files (x86)",
        r"C:\\Users\\%USERNAME%\\AppData\\Local\\Programs",
    ]
    best_match = None
    highest_score = 0

    for directory in common_dirs:
        for root, _, files in os.walk(os.path.expandvars(directory)):
            for file in files:
                if file.endswith('.exe'):
                    score = fuzz.ratio(app_name, file.lower())
                    if app_name in file.lower():  # Prioritize substring matches
                        score += 20
                    if score > highest_score:
                        best_match = os.path.join(root, file)
                        highest_score = score

    if best_match and highest_score > 75:
        return best_match
    return None