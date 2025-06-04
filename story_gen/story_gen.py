"""
Enhanced Story Generation Logic with Controlled Creativity and Focus Modes
"""

from .story_utils import polish_chunk, parse_streamed_response, get_generation_params, OLLAMA_API_URL
import requests

def generate_story(caption, genre="General", current_story="", user_instruction="", 
                   max_chunk_words=500, nearing_end=False, ending=False, 
                   creativity_level="balanced", consistency_mode=False, focus_mode="balanced"):
    """
    Generate story chunks with enhanced control parameters.
    """
    temperature, top_p, repeat_penalty, top_k = get_generation_params(creativity_level, consistency_mode=consistency_mode)

    num_predict, num_ctx = _adjust_context_and_length(current_story, ending)

    prompt = _build_prompt(caption, genre, current_story, user_instruction, 
                           max_chunk_words, nearing_end, ending, focus_mode)

    payload = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "repeat_penalty": repeat_penalty,
            "num_ctx": num_ctx,
            "num_predict": num_predict,
            "stop": ["THE END", "End of story", "---"],
            "seed": -1 if creativity_level == "creative" else 42,
        }
    }

    print(f"[INFO] Generating story chunk with {creativity_level} creativity, {focus_mode} focus...")
    print(f"[INFO] Parameters: temp={temperature:.2f}, top_p={top_p:.2f}, repeat_penalty={repeat_penalty:.2f}")
    
    response = requests.post(OLLAMA_API_URL, json=payload, stream=True)
    response.raise_for_status()

    story_chunk = parse_streamed_response(response)

    return polish_chunk(story_chunk, creativity_level)


# ---- Helper functions ----

def _adjust_context_and_length(current_story, ending):
    if ending:
        return 800, 8192
    elif not current_story:
        return 700, 4096
    else:
        return 600, 6144


def _build_prompt(caption, genre, current_story, user_instruction, max_chunk_words, nearing_end, ending, focus_mode):
    focus_instructions = {
        "descriptive": "Focus on vivid descriptions and sensory details.",
        "dialogue": "Emphasize character interactions and dialogue.",
        "action": "Focus on dynamic scenes and plot progression.",
        "balanced": "Balance description, dialogue, and action."
    }

    if ending:
        instruction = (
            f"Write a conclusion to the story ensuring coherence and matching tone.\n"
            f"{focus_instructions.get(focus_mode, '')}\n\nCURRENT STORY:\n{current_story}\n\nWrite the conclusion:"
        )
    elif not current_story:
        instruction = (
            f"Write a {genre} story based on:\n\"{caption}\"\n\n"
            f"{focus_instructions.get(focus_mode, '')}"
        )
    else:
        story_instruction = (
            "Wrap up the story subtly." if nearing_end else "Advance the plot with new events."
        )
        instruction = (
            f"USER INSTRUCTIONS:\n{user_instruction or 'Continue normally.'}\n\n"
            f"{story_instruction}\n"
            f"{focus_instructions.get(focus_mode, '')}\n\n"
            f"CURRENT STORY:\n{current_story[-3000:]}\n\nContinue writing:"
        )

    return instruction