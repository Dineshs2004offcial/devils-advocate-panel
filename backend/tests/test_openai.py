import sys
from pathlib import Path

# Add backend directory to sys.path so 'app' can always be resolved
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.llm.openai import get_openai


llm = get_openai()

response = llm.invoke(
    "You are a financial analyst. Ask one short question about a startup pitch."
)

print(response.content)
