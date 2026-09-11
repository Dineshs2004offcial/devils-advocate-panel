
import sys
from pathlib import Path

import pytest

# Add backend directory to sys.path so 'app' can always be resolved
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.llm.gemini import get_gemini


def test_gemini_factory():
    """Verify that the Gemini LLM can be created without making an API call."""
    llm = get_gemini()

    assert llm is not None
    assert hasattr(llm, "invoke")


@pytest.mark.skip(reason="Requires live Gemini API and consumes API quota")
def test_gemini_live():
    """Optional live Gemini API test."""
    llm = get_gemini()

    response = llm.invoke(
        "You are a skeptical VC. Give one short question about a startup pitch."
    )

    assert response.content
