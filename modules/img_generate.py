import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv


load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HuggingFace token not found in .env file")

def generate_img(command):
    
    prompt = command.replace("generate image for", "").strip()
    
    client = InferenceClient(token=HF_TOKEN)

    try:
        image = client.text_to_image(
            prompt=prompt,
            model="runwayml/stable-diffusion-v1-5"
        )
           
        documents_path = os.path.join(os.path.expanduser("~"), "Documents")
        
        if not os.path.exists(documents_path):
            os.makedirs(documents_path)
        
        filename = os.path.join(documents_path, f"{prompt.replace(' ', '_')}.png")
        image.save(filename)
        
        image.show()
        print(f"Image saved in Documents as {filename}.")
        
        return filename
    except Exception as e:
        print(f"Error generating image: {e}")
        return None
