from langchain_mistralai import ChatMistralAI
from app.core.config import settings


def get_mistral():
    return ChatMistralAI(
        model=settings.MISTRAL_MODEL,
        api_key=settings.MISTRAL_API_KEY,
    )
