import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-small-latest")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


settings = Settings()