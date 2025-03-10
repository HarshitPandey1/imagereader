from dotenv import load_dotenv
import os
import base64
from groq import Groq

load_dotenv()

# Configure Groq
client = Groq(api_key="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")

def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print("Error: Image file not found.")
        return None

def get_groq_response(task, base64_image):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": task},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="llama-3.2-11b-vision-preview",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def save_to_file(response, filename="models.py"):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("from sqlalchemy import Column, Integer, String\n")
            file.write("from sqlalchemy.ext.declarative import declarative_base\n\n")
            file.write("Base = declarative_base()\n\n")
            file.write(response)
        print(f"ORM model saved to {filename}")
    except Exception as e:
        print(f"Error saving file: {str(e)}")

def main():
    image_path = "./schema.jpg"
    base64_image = encode_image(image_path)
    if base64_image is None:
        return
    
    print("Image to ORM Model Generator with Groq")
    print("Type 'exit' to quit the program")
    print("-" * 50)
    
    while True:
        task = "Generate SQLAlchemy ORM classes from this schema"
        
        print("\nProcessing your request...")
        response = get_groq_response(task, base64_image)
        
        if response:
            save_to_file(response)
            print("\nGenerated ORM model:")
            print("-" * 50)
            print(response)
            print("-" * 50)
        else:
            print("No response received")
        
        break

if __name__ == "__main__":
    main()
