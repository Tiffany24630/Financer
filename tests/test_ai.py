from types import SimpleNamespace
from unittest.mock import MagicMock, patch
import pytest
from ia.openai_service import analyze_financial_data, ask_assistant

def make_openai_response(content):
    return SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(content=content)
            )
        ]
    )

def make_mock_client(response):
    client = MagicMock()
    client.chat.completions.create.return_value = response
    return client

def test_analyze_financial_data_builds_request_and_returns_content():
    client = make_mock_client(make_openai_response("Resumen generado"))

    with patch("ia.openai_service.get_openai_client", return_value=client):
        result = analyze_financial_data("ventas\n100")

    assert result == "Resumen generado"
    client.chat.completions.create.assert_called_once()

    request = client.chat.completions.create.call_args.kwargs
    assert request["model"] == "gpt-4o"
    assert request["messages"][0] == {
        "role": "system",
        "content": "Eres un contador experto en Guatemala.",
    }
    assert request["messages"][1]["role"] == "user"
    assert "ventas\n100" in request["messages"][1]["content"]
    assert "ISR estimado" in request["messages"][1]["content"]
    assert "IVA estimado" in request["messages"][1]["content"]

def test_ask_assistant_includes_question_and_financial_context():
    client = make_mock_client(make_openai_response("Respuesta generada"))

    with patch("ia.openai_service.get_openai_client", return_value=client):
        result = ask_assistant(
            "¿Cuál fue la venta total?",
            "ventas: 100",
        )

    assert result == "Respuesta generada"
    request = client.chat.completions.create.call_args.kwargs
    prompt = request["messages"][1]["content"]
    assert "ventas: 100" in prompt
    assert "¿Cuál fue la venta total?" in prompt

def test_ai_services_return_empty_string_for_empty_model_content():
    client = make_mock_client(make_openai_response(None))

    with patch("ia.openai_service.get_openai_client", return_value=client):
        assert analyze_financial_data("datos") == ""

def test_ai_service_propagates_openai_errors():
    client = MagicMock()
    client.chat.completions.create.side_effect = RuntimeError("OpenAI unavailable")

    with patch("ia.openai_service.get_openai_client", return_value=client):
        with pytest.raises(RuntimeError, match="OpenAI unavailable"):
            ask_assistant("pregunta", "contexto")