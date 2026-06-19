from dotenv import load_dotenv
from google import genai
from groq import Groq
import os
load_dotenv()

PROMPT = "Explain what a large language model is in 2 sentences."

def call_gemini(prompt):
    client = genai.Client()
    response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
    )
    return response.text
    pass

def call_groq(prompt):
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
    pass

if __name__ == "__main__":
    print("==Gemini==")
    print(call_gemini(PROMPT))
    print("==groq==")
    print(call_groq(PROMPT))




