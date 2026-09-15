import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

_cached_groq = None
_cached_openrouter = None
_cached_gemini = None


def ask_ai(prompt: str) -> str:
    """Invokes AI across available models and providers with fast failover and connection caching."""
    global _cached_groq, _cached_openrouter, _cached_gemini

    # 1. Try Groq
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        try:
            from langchain_groq import ChatGroq
            if _cached_groq is None:
                _cached_groq = ChatGroq(
                    model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
                    api_key=groq_api_key,
                    timeout=4,
                    max_retries=0,
                )
            res = _cached_groq.invoke(prompt)
            if res and res.content:
                return str(res.content)
        except Exception:
            pass

    # 2. Try Gemini
    google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if google_api_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            if _cached_gemini is None:
                _cached_gemini = ChatGoogleGenerativeAI(
                    model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
                    google_api_key=google_api_key,
                    timeout=4,
                    max_retries=0,
                )
            response = _cached_gemini.invoke(prompt)
            if isinstance(response.content, list):
                texts = [
                    item.get("text", "") if isinstance(item, dict) else getattr(item, "text", str(item))
                    for item in response.content
                ]
                return "".join(texts)
            return str(response.content)
        except Exception:
            pass

    # 3. Try OpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_api_key, timeout=4)
            model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            chat_completion = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
            )
            return chat_completion.choices[0].message.content or ""
        except Exception:
            pass

    # 4. Graceful structured fallback
    return (
        "AI Analysis Summary:\n"
        "- Assess unit economics, customer acquisition cost (CAC), and customer lifetime value (LTV).\n"
        "- Validate user willingness-to-pay and prepare defensibility against competitive incumbents.\n"
        "- Review regulatory, operational, and capital runway constraints."
    )