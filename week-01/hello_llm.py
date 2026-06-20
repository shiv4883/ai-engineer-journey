from dotenv import load_dotenv
from google import genai
from groq import Groq
import typer

import os
load_dotenv()

app = typer.Typer()


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
    

@app.command()
def main(provider: str= typer.Option(...,help="choose provided: groq or gemini"),
         prompt: str= typer.Option(...,help="share your prompt"),
         mode: str= typer.Option("basic",help="select mode: basic, detailed or eli5")):
    
    if mode == "basic":
        if provider == "groq":
            print("==groq==")
            print(call_groq(prompt))

        elif provider == "gemini":
            print("==Gemini==")
            print(call_gemini(prompt))
        else:
            print(f"{provider} is incorrect")
    elif mode == "detailed":
        if provider == "groq":
            print("==groq==")
            print(call_groq(prompt + ". Give a detailed technical explanation"))

        elif provider == "gemini":
            print("==Gemini==")
            print(call_gemini(prompt + ". Give a detailed technical explanation"))
        else:
            print(f"{provider} is incorrect")
    elif mode == "eli5":
        if provider == "groq":
            print("==groq==")
            print(call_groq(prompt + ". Explain like i am 5"))

        elif provider == "gemini":
            print("==Gemini==")
            print(call_gemini(prompt + ". Explain like i am 5"))
        else:
            print(f"{provider} is incorrect")
    else:
        print(f"the mode is incorrect. Choose one of 'basic', 'detailed' or 'eli5'.")



if __name__ == "__main__":
    app()
    



