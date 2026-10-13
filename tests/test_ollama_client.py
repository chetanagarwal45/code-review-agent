from models.ollama_client import OllamaClient


def test_build_prompt_wraps_code_block():
    client = OllamaClient()
    prompt = client._build_prompt("print('ok')", "python")

    assert "```python" in prompt
    assert "print('ok')" in prompt
    assert prompt.rstrip().endswith("```")
