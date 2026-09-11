import sys
from pathlib import Path

import pytest

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.llm.openai import get_openai


def test_openai_factory():
    """Verify OpenAI can be created without making an API call."""
    llm = get_openai()

    assert llm is not None
    assert hasattr(llm, "invoke")


@pytest.mark.skip(reason="Requires live OpenAI API and consumes API credits")
def test_openai_live():
    """Optional live OpenAI API test."""
    llm = get_openai()

    response = llm.invoke(
        "You are a financial analyst. Ask one short question about a startup pitch."
    )

    assert response.content