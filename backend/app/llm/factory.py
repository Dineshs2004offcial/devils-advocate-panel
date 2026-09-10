from app.llm.gemini import get_gemini
from app.llm.openai import get_openai
from app.llm.mistral import get_mistral


def get_llm(provider: str = "gemini"):
    provider = provider.lower()
    if provider == "openai":
        return get_openai()
    elif provider == "mistral":
        return get_mistral()
    elif provider == "gemini":
        return get_gemini()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
