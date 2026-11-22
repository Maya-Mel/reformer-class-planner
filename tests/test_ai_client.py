from google.genai import errors
import pytest
import ai_client


def test_quota_error_moves_to_next_model(monkeypatch):
    tried_models = []

    def fake_generate_content(model, contents, config):
        tried_models.append(model)
        if model == ai_client.MODELS[0]:
            raise errors.ClientError(429, {"error": {"code": 429, "message": "quota", "status": "RESOURCE_EXHAUSTED"}})
        return "OK"

    monkeypatch.setattr(ai_client.client.models, "generate_content", fake_generate_content)

    result = ai_client.generate_with_fallback("hello", None)

    assert result == "OK"
    assert tried_models == [ai_client.MODELS[0], ai_client.MODELS[1]]

def test_other_client_errors_do_not_move_to_next_model(monkeypatch):
    tried_models = []
    
    def fake_generate_content(model, contents, config):
        tried_models.append(model)
        if model == ai_client.MODELS[0]:
            raise errors.ClientError(400, {"error": {"code": 400, "message": "bad request", "status": "INVALID_ARGUMENT"}})

    monkeypatch.setattr(ai_client.client.models, "generate_content", fake_generate_content)
    with pytest.raises(errors.ClientError):
        ai_client.generate_with_fallback("hello", None)

    assert tried_models == [ai_client.MODELS[0]]
    