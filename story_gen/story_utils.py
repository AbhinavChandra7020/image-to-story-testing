"""
Common utilities for story generation modules.
"""

import requests
import json

# API endpoint for Ollama server
OLLAMA_API_URL = "http://localhost:11434/api/generate"


def polish_chunk(chunk, creativity_level="balanced"):
    """
    Polishes a story chunk to enhance readability and format it into paragraphs.
    """
    temp, top_p, rep_penalty = get_polish_params(creativity_level)

    payload = {
        "model": "llama3.1:8b",
        "prompt": (
            "You are a professional novel editor. Fix the grammar, enhance readability, and format the text into natural paragraphs. "
            "Preserve the original meaning and tone. Output ONLY the corrected story text WITHOUT any explanation, introduction, or notes. "
            "Just the pure polished story.\n\n"

            f"Text:\n{chunk}\n\nPolished Story Text:"
        ),
        "stream": True,
        "options": {
            "temperature": temp,
            "top_p": top_p,
            "repeat_penalty": rep_penalty,
            "num_ctx": 4096,
            "num_predict": 1000,
        }
    }

    print(f"[INFO] Polishing chunk with creativity level '{creativity_level}'...")
    response = requests.post(OLLAMA_API_URL, json=payload, stream=True)
    response.raise_for_status()

    return parse_streamed_response(response)


def parse_streamed_response(response):
    """
    Parses a streamed response from the Ollama API.
    """
    text = ""
    for line in response.iter_lines():
        if line:
            parsed = json.loads(line.decode('utf-8'))
            text += parsed.get("response", "")
    return text.strip()


def get_polish_params(creativity_level):
    """
    Returns polishing parameters based on the creativity level.
    """
    params = {
        "conservative": (0.3, 0.7, 1.1),
        "creative": (0.9, 0.95, 1.05),
        "balanced": (0.6, 0.8, 1.1)
    }
    return params.get(creativity_level, params["balanced"])


def get_generation_params(creativity_level, consistency_mode=False, one_shot_mode=False):
    """
    Returns generation parameters based on creativity level.
    If `one_shot_mode` is True, use one-shot specific defaults.
    """
    if one_shot_mode:
        params = {
            "conservative": (0.6, 0.8, 1.15, 30),
            "creative": (0.9, 0.95, 1.05, 80),
            "balanced": (0.75, 0.85, 1.1, 50)
        }
    else:
        params = {
            "conservative": (0.4, 0.7, 1.15, 20),
            "creative": (0.9, 0.95, 1.05, 80),
            "balanced": (0.7, 0.85, 1.1, 40)
        }

    temperature, top_p, repeat_penalty, top_k = params.get(creativity_level, params["balanced"])

    if consistency_mode and not one_shot_mode:
        temperature *= 0.8
        repeat_penalty += 0.05
        top_p *= 0.9

    return temperature, top_p, repeat_penalty, top_k