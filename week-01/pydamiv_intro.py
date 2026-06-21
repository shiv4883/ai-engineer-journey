from pydantic import BaseModel

class LLMResponse(BaseModel):
    provider: str
    prompt: str
    response: str

def wrap_response(provider: str, prompt: str, response: str) -> LLMResponse:
    return LLMResponse(provider=provider, prompt=prompt, response=response)

result = wrap_response(
    provider="groq",
    prompt="What is RAG?",
    response="RAG stands for Retrieval Augmented Generation..."
)

print(result)
print(result.response)