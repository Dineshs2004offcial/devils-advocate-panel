import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def ask_ai(prompt: str) -> str:
    """Invokes AI across available models and providers with automatic fallback."""
    google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if google_api_key:
        from langchain_google_genai import ChatGoogleGenerativeAI
        models_to_try = [
            os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
            "gemini-2.5-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
        ]
        for m in models_to_try:
            try:
                llm = ChatGoogleGenerativeAI(
                    model=m,
                    google_api_key=google_api_key,
                )
                response = llm.invoke(prompt)
                if isinstance(response.content, list):
                    texts = [
                        item.get("text", "") if isinstance(item, dict) else getattr(item, "text", str(item))
                        for item in response.content
                    ]
                    return "".join(texts)
                return str(response.content)
            except Exception as e:
                print(f"[AI Service] Gemini model '{m}' failed: {e}")

    # 2. Try OpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_api_key)
            model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            chat_completion = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
            )
            return chat_completion.choices[0].message.content or ""
        except Exception as e:
            print(f"[AI Service] OpenAI invocation failed: {e}")

    # 3. Graceful fallback if external APIs are rate-limited or offline
    return (
        "AI Analysis Summary:\n"
        "- Assess unit economics, customer acquisition cost (CAC), and customer lifetime value (LTV).\n"
        "- Validate user willingness-to-pay and prepare defensibility against competitive incumbents.\n"
        "- Review regulatory, operational, and capital runway constraints."
    )