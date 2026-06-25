from google import genai
from groq import Groq
import typer
import dotenv
import pydantic
import os
import json

dotenv.load_dotenv()


class ResponseFormat(pydantic.BaseModel):
    Answer: str
    confidence: str
    key_terms: list[str]


def call_gemini(prompt: str, is_json: bool = False) -> str:
    try:
        client = genai.Client()
        args = {"model":"gemini-2.5-flash", "input":prompt}
        
        if is_json:
            args["response_format"] = {"type": "text", "mime_type": "application/json"}
       # response = ResponseFormat(**interaction)
        interaction = client.interactions.create(**args)
        return interaction.output_text
    except Exception as e:
        print(e)


def call_groq(prompt: str, is_json: bool = False) -> str:
    try:
        client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
            )
        
        args = {"messages": [{"role": "user", "content": prompt}], "model": "llama-3.3-70b-versatile",}
        if is_json:
            args["response_format"]={"type": "json_object"}
    #  response = ResponseFormat(**interaction)
        interaction = client.chat.completions.create(**args)
        parsed = interaction.choices[0].message.content
        return parsed
    except Exception as e:
        print (e)

    
app = typer.Typer()

@app.command()
def main(prompt:str = typer.Option(..., help = """the prompt"""),
         provider:str = typer.Option(..., help = """the provider"""),
         mode:str=typer.Option(..., help = """the mode""")):
    mode=mode.lower()
    provider=provider.lower()
    
    mode_def = {
        "basic": "",
        "detailed": "give technical details",
        "eli5": "Explain it like i am 5 years old",
        "json": "Return the response in JSON format with the following 3 keys only: Answer, confidence (low/medium/high) and key_terms(ket terms in the answer as list of strings.) "
    }
    if mode not in mode_def:
        typer.secho(f"Invalid mode: {mode}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    final_prompt = prompt + mode_def[mode]
    if provider == "groq":
        typer.secho("==GROQ==",fg=typer.colors.MAGENTA)
        if mode == "json":
           parsed=json.loads(call_groq(final_prompt,True))
           #print(parsed)
           final = ResponseFormat(**parsed)
           print(final)
           

        else:
            print(call_groq(final_prompt))


        
    elif provider == "gemini":
        typer.secho("==GEMINI==",fg=typer.colors.GREEN)
        if mode == "json":
           parsed=json.loads(call_gemini(final_prompt,True))
           #print(parsed)
           final = ResponseFormat(**parsed)
           print(final)
        else:
            print(call_gemini(final_prompt))

    else:
        print(f'provider {provider} is incorrect')
if __name__ == '__main__':
    app()