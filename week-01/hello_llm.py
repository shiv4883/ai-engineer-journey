from dotenv import load_dotenv
from google import genai
from groq import Groq
import os
load_dotenv()

PROMPT = "Explain what a large language model is in 2 sentences."

def call_gemini(prompt: str) -> str:
    client = genai.Client()
    try:
        response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt 
        )
        return response.text
    except Exception as e:
        return f"Gemini Error: {e}"
    

def call_groq(prompt: str) -> str:
    try:
        client = Groq()
        chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"groq Error: {e}"
    

if __name__ == "__main__":
    print("==Gemini==")
    print(call_gemini(PROMPT))
    print("==groq==")
    print(call_groq(PROMPT))




