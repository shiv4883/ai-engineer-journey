from dotenv import load_dotenv
from google import genai
from groq import Groq
import typer

import os
from pydantic import BaseModel

class LLMResponse(BaseModel):
    provider: str
    prompt: str
    response: str


load_dotenv()

app = typer.Typer(rich_help_panel="Utils")


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
    
    """
    An AI Engineer CLI tool to query multiple LLM providers with different processing modes.
    """
    provider = provider.lower()
    mode = mode.lower()

    # 2. Map and inject your system behavior modifications based on mode
    mode_modifiers = {
        "basic": "",
        "detailed": ". Give a detailed technical explanation.",
        "eli5": ". Explain like I am 5 years old.",

    }

    if mode not in mode_modifiers:
        typer.secho(f"Error: Mode '{mode}' is incorrect. Choose 'basic', 'detailed', or 'eli5'.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    # Modify the prompt once right here
    final_prompt = prompt + mode_modifiers[mode]

    # 3. Route to the correct provider cleanly
    if provider == "groq":
        typer.secho("== Groq ==", fg=typer.colors.CYAN, bold=True)
        raw = call_groq(final_prompt)
        result = LLMResponse (provider=provider,prompt=prompt,response=raw)
        print(result.response)
        
    elif provider == "gemini":
        typer.secho("== Gemini ==", fg=typer.colors.GREEN, bold=True)
        raw = call_gemini(final_prompt)
        result = LLMResponse (provider=provider,prompt=prompt,response=raw)
        print(result.response)
        
    else:
        typer.secho(f"Error: Provider '{provider}' is incorrect. Use 'groq' or 'gemini'.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
    



