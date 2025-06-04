import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def generate_title(story_text, genre="General"):
    """Generate multiple title options for the story and let the user choose."""
    payload = {
        "model": "llama3.1:8b",
        "prompt": (
            f"You are a professional book title creator. Given the following {genre} story, "
            "generate 5 creative, compelling, and short title options (max 10 words each). "
            "Avoid generic titles. Make them intriguing and genre-appropriate. Number each option clearly.\n\n"
            f"Story:\n{story_text}\n\nTitle options:"
        ),
        "stream": False
    }

    print("[INFO] Generating title options for the story...")
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()

    titles_block = response.json().get("response", "").strip()

    # title options
    print("\nHere are the title options:\n")
    print(titles_block)
    print("\nPlease choose a title by entering its number (e.g., 1, 2, 3, etc.):")
    choice = input("Your choice: ").strip()

    # title list
    titles = []
    for line in titles_block.split("\n"):
        if line.strip().startswith(("1.", "2.", "3.", "4.", "5.")):
            title = line.split(".", 1)[1].strip(" \"")
            titles.append(title)

    try:
        chosen_title = titles[int(choice) - 1]
    except (IndexError, ValueError):
        print("[WARNING] Invalid choice. Defaulting to the first title.")
        chosen_title = titles[0] if titles else "Untitled Story"

    return chosen_title
