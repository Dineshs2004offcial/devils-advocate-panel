import os

from app.core.config import settings
from app.llm.gemini import get_gemini
from app.llm.mistral import get_mistral
from app.llm.openai import get_openai
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


def get_llm(provider: str = "gemini", model: str | None = None):
    provider = provider.lower()

    if provider == "openai":
        return get_openai()

    elif provider == "mistral":
        return get_mistral()

    elif provider == "gemini":
        return get_gemini()

    elif provider == "groq":
        return ChatGroq(
            model=model or settings.GROQ_MODEL,
            temperature=0,
            max_tokens=2048,
            api_key=settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY"),
        )

    elif provider == "openrouter":
        return ChatOpenAI(
            model=model or settings.OPENROUTER_MODEL,
            temperature=0,
            api_key=settings.OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")




def invoke_with_fallback(prompt: str, model: str | None = None):
    providers = ["groq", "openrouter", "gemini"]

    last_error = None

    for provider in providers:
        try:
            llm = get_llm(provider, model=model)
            return llm.invoke(prompt)

        except Exception as error:
            print(f"{provider} failed: {error}")
            last_error = error

    raise RuntimeError(
        "All configured LLM providers failed."
    ) from last_error
