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

def main():
    image_path = "./schema.jpg"
    base64_image = encode_image(image_path)
    if base64_image is None:
        return
    
    print("Image Processing Assistant with Groq")
    print("Type 'exit' to quit the program")
    print("-" * 50)
    
    while True:
        task = input("\nEnter your task: ").strip()
        
        if task.lower() in ['q', 'quit', 'exit']:
            print("Goodbye!")
            break
        
        if task:
            print("\nProcessing your request...")
            response = get_groq_response(task, base64_image)
            
            if response:
                print("\nResponse:")
                print("-" * 50)
                print(response)
                print("-" * 50)
            else:
                print("No response received")
        else:
            print("Please enter a valid task")

if __name__ == "__main__":
    main()
