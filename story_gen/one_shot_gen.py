"""
One-Shot Story Generation Logic with Progress Saving
"""

from .story_utils import polish_chunk, parse_streamed_response, get_generation_params, OLLAMA_API_URL
import requests
import json

def generate_one_shot_story(caption, genre="General", max_words=5000, 
                             creativity_level="balanced", output_file="results.txt",
                             chunk_size=800, max_attempts=20,
                             consistency_mode=False, focus_mode="balanced"):
    """
    Generate a full-length story by stitching together multiple chunks.
    Progress is saved iteratively to a file after each chunk.
    """
    temperature, top_p, repeat_penalty, top_k = get_generation_params(
        creativity_level,
        consistency_mode=consistency_mode,
        one_shot_mode=True
    )

    if not caption:
        raise ValueError("Caption must not be empty.")

    total_words_generated = 0
    chunk_count = 0
    story = ""

    # Clear previous file if exists
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Story Generation Progress\n{'='*30}\n\n")

    print(f"[INFO] Starting one-shot story generation...")
    print(f"[INFO] Target: {max_words} words, Chunk size: ~{chunk_size} words")

    while total_words_generated < max_words and chunk_count < max_attempts:
        chunk_count += 1
        words_remaining = max_words - total_words_generated
        
        nearing_end = total_words_generated >= 0.85 * max_words
        
        if nearing_end:
            current_chunk_target = min(words_remaining, chunk_size // 2)
            generation_instruction = "conclusion"
        elif words_remaining < chunk_size:
            current_chunk_target = words_remaining
            generation_instruction = "final"
        else:
            current_chunk_target = chunk_size
            generation_instruction = "continue"

        prompt = _build_prompt(caption, genre, story, current_chunk_target, generation_instruction, focus_mode)

        payload = {
            "model": "llama3.1:8b",
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "repeat_penalty": repeat_penalty,
                "num_ctx": 6144,
                "num_predict": current_chunk_target + 200,
                "stop": ["THE END", "End of story", "---"] if generation_instruction == "final" else [],
            }
        }

        print(f"[CHUNK {chunk_count}] Generating ~{current_chunk_target} words ({generation_instruction})...")
        response = requests.post(OLLAMA_API_URL, json=payload, stream=True)
        response.raise_for_status()

        story_chunk = parse_streamed_response(response)
        polished_chunk = polish_chunk(story_chunk.strip(), creativity_level)

        # Save after every polished chunk
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(polished_chunk + "\n\n")

        story += "\n\n" + polished_chunk if story else polished_chunk
        total_words_generated = len(story.split())

        print(f"[PROGRESS] {total_words_generated}/{max_words} words ({(total_words_generated / max_words) * 100:.1f}%)")

        if total_words_generated >= max_words:
            print(f"[SUCCESS] Target word count reached!")
            break
        
        if chunk_count > 1 and len(polished_chunk.split()) < 50:
            print(f"[WARNING] Chunk {chunk_count} generated only {len(polished_chunk.split())} words")

    return story


def _build_prompt(caption, genre, story_so_far, chunk_target, generation_instruction, focus_mode="balanced"):
    """
    Build a dynamic prompt based on the current generation stage with focus instructions.
    """
    focus_instructions = {
        "descriptive": "Focus on vivid descriptions and sensory details.",
        "dialogue": "Emphasize character interactions and dialogue.",
        "action": "Focus on dynamic scenes and plot progression.",
        "balanced": "Balance description, dialogue, and action."
    }
    focus_text = focus_instructions.get(focus_mode, "Balance description, dialogue, and action.")

    if generation_instruction == "conclusion":
        return (
            f"You are a critically acclaimed novelist. "
            f"Begin concluding the story gracefully based on the content written so far. "
            f"Write approximately {chunk_target} words.\n\n"
            f"{focus_text}\n\n"
            f"Description: \"{caption}\"\n\n"
            f"Story so far:\n{story_so_far[-4000:]}\n\n"
            f"Continue the story toward its conclusion:"
        )
    elif generation_instruction == "final":
        return (
            f"You are a critically acclaimed novelist. "
            f"Write the final {chunk_target} words to complete this story. "
            f"Provide a satisfying, coherent ending.\n\n"
            f"{focus_text}\n\n"
            f"Description: \"{caption}\"\n\n"
            f"Story so far:\n{story_so_far[-4000:]}\n\n"
            f"Write the ending:"
        )
    else:
        if not story_so_far:
            return (
                f"You are a critically acclaimed novelist. "
                f"Write the beginning of a {genre} story based on this description. "
                f"Write approximately {chunk_target} words.\n\n"
                f"{focus_text}\n\n"
                f"Description: \"{caption}\"\n\n"
                f"Begin the story:"
            )
        else:
            return (
                f"You are a critically acclaimed novelist. "
                f"Continue this {genre} story by developing the plot further. "
                f"Write approximately {chunk_target} words.\n\n"
                f"{focus_text}\n\n"
                f"Description: \"{caption}\"\n\n"
                f"Story so far:\n{story_so_far[-4000:]}\n\n"
                f"Continue the story:"
            )
