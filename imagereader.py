from groq import Groq
import base64

def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print("Error: Image file not found.")
        return None

def main():
    image_path = "./schema.jpg"
    base64_image = encode_image(image_path)
    if base64_image is None:
        return
    
    api_key = "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"
    client = Groq(api_key=api_key)
    
    while True:
        task = input("Enter the task (or type 'q' or 'quit' to exit): ")
        if task.lower() in ['q', 'quit']:
            print("Exiting the program.")
            break
        
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
        
        print("Response:")
        print(chat_completion.choices[0].message.content)

if __name__ == "__main__":
    main()