from image_caption import generate_caption
from story_gen import generate_story, generate_one_shot_story, generate_title
from ui.ui import setup_window, update_window, show_completion_message, update_status
import os
import random

def select_random_image(image_folder="images"):
    images = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        raise FileNotFoundError(f"No images found in '{image_folder}' folder.")
    selected_image = random.choice(images)
    print(f"[INFO] Selected random image: {selected_image}")
    return os.path.join(image_folder, selected_image)

def interactive_mode(caption, genre, max_words, creativity_level, consistency_mode, focus_mode):
    window, text_widget = setup_window()
    current_story = ""
    current_word_count = 0
    previous_instructions = []

    # initialization
    update_status(window, "Initializing story generation...", "#89b4fa")

    continue_generation = True
    chunk_number = 1
    
    while continue_generation and (max_words is None or current_word_count < max_words):
        # progress status
        update_status(window, f"Generating story chunk {chunk_number}...", "#f9e2af")
        
        nearing_end = (max_words is not None) and (current_word_count >= 0.9 * max_words)
        bullet_points = "\n".join(f"• {instr.strip()}" for instr in previous_instructions) if previous_instructions else ""

        story_chunk = generate_story(
            caption=caption,
            genre=genre,
            current_story=current_story,
            user_instruction=bullet_points,
            max_chunk_words=500,
            nearing_end=nearing_end,
            creativity_level=creativity_level,
            consistency_mode=consistency_mode,
            focus_mode=focus_mode
        )
        
        current_story += "\n\n" + story_chunk
        current_word_count = len(current_story.split())
        update_window(window, text_widget, current_story)
        
        progress_percent = min(100, (current_word_count / max_words * 100)) if max_words else 0
        if max_words:
            update_status(window, f"Progress: {current_word_count:,}/{max_words:,} words ({progress_percent:.1f}%)", "#89b4fa")
        else:
            update_status(window, f"Story length: {current_word_count:,} words", "#89b4fa")

        # mid story change
        print("\n--- Current Settings ---")
        print(f"Creativity Level: {creativity_level}")
        print(f"Consistency Mode: {'On' if consistency_mode else 'Off'}")
        print(f"Focus Mode: {focus_mode}\n")

        print("--- Adjust Story Generation Settings ---")
        print("Creativity Levels:")
        print("  1. Conservative - Logical and grounded storytelling.")
        print("  2. Balanced - Mix of creativity and structure.")
        print("  3. Creative - Wild, unexpected ideas.\n")

        print("Consistency Mode (yes/no):")
        print("  Ensures logical continuity in the story.\n")

        print("Focus Modes:")
        print("  1. Descriptive - Vivid scene descriptions.")
        print("  2. Dialogue - Emphasis on character conversations.")
        print("  3. Action - Dynamic and event-driven storytelling.")
        print("  4. Balanced - A mix of description, dialogue, and action.\n")

        change_settings = input("Would you like to change creativity/focus/consistency? (yes/no): ").strip().lower()

        if change_settings == "yes":
            creativity_choice = input("Choose Creativity Level (1-3): ").strip()
            creativity_level = {"1": "conservative", "2": "balanced", "3": "creative"}.get(creativity_choice, creativity_level)

            consistency_input = input("Enable Consistency Mode? (yes/no): ").strip().lower()
            consistency_mode = consistency_input == "yes"

            focus_choice = input("Choose Focus Mode (1-4): ").strip()
            focus_mode = {"1": "descriptive", "2": "dialogue", "3": "action", "4": "balanced"}.get(focus_choice, focus_mode)

        print("\n")

        if max_words is not None and current_word_count >= max_words:
            print(f"\n[INFO] Maximum word limit ({max_words} words) reached.")
            update_status(window, "Word limit reached. Generating final conclusion...", "#f38ba8")
            break

        print("\nWould you like to continue, change genre, suggest changes, change+suggest, or stop?")
        user_choice = input("Type 'continue', 'change', 'suggest', 'change+suggest', or 'stop': ").strip().lower()

        if user_choice == "stop":
            update_status(window, "Generating story conclusion...", "#f9e2af")
            final_chunk = generate_story(
                caption=caption,
                genre=genre,
                current_story=current_story,
                user_instruction="",
                ending=True,
                creativity_level=creativity_level,
                consistency_mode=consistency_mode,
                focus_mode=focus_mode
            )
            current_story += "\n\n" + final_chunk
            update_window(window, text_widget, current_story)
            break
        elif user_choice == "change":
            genre = input("Enter the new genre you want to switch to: ").strip()
            update_status(window, f"Genre changed to: {genre}", "#a6e3a1")
        elif user_choice == "suggest":
            new_instruction = input("Enter your suggestion for the next part of the story: ").strip()
            previous_instructions.append(new_instruction)
            update_status(window, "User suggestion added", "#a6e3a1")
        elif user_choice == "change+suggest":
            genre = input("Enter the new genre you want to switch to: ").strip()
            new_instruction = input("Enter your suggestion for the next part of the story: ").strip()
            previous_instructions.append(new_instruction)
            update_status(window, f"Genre changed to {genre} and suggestion added", "#a6e3a1")
        
        chunk_number += 1

    # completion message
    show_completion_message(window)
    window.mainloop()
    return current_story

def main(output_file='result.txt'):
    print("[INFO] Starting Image Caption and Story Generation Pipeline...")

    user_image_path = input("Enter the image path (leave blank for random selection): ").strip()

    if user_image_path:
        image_path = user_image_path
    else:
        image_path = select_random_image()

    print("\nChoose Story Generation Mode:")
    print("1. One-Shot Mode (full story at once)")
    print("2. Interactive Mode (step-by-step with suggestions)")
    mode_choice = input("Enter 1 or 2: ").strip()

    print("\nChoose caption detail level:")
    print("1. Very Detailed Caption (full scene, objects, surroundings)")
    print("2. Short Caption (2-3 sentences, main subject only)")
    detail_choice = input("Enter 1 for Detailed or 2 for Short: ").strip()

    detail_level = "short" if detail_choice == "2" else "detailed"

    caption = generate_caption(image_path, detail_level)
    print(f"\n[CAPTION]: {caption}")

    genre = input("\nChoose a genre for your story (e.g., Horror, Sci-Fi, Fantasy, Romance, Comedy): ").strip()

    user_input = input("\nSet the maximum word limit for your story (default is 8000 words): ").strip().lower()
    try:
        max_words = int(user_input)
    except ValueError:
        print("Invalid input. Setting default limit to 8000 words.")
        max_words = 8000

    # options
    print("\nChoose creativity level:")
    print("1. Conservative - Logical and grounded storytelling. Less surprises.")
    print("2. Balanced - Mix of creativity and structure. Good for most genres.")
    print("3. Creative - Wild, unexpected ideas. Higher randomness.")
    creativity_choice = input("Enter 1, 2, or 3: ").strip()
    creativity_map = {"1": "conservative", "2": "balanced", "3": "creative"}
    creativity_level = creativity_map.get(creativity_choice, "balanced")

    print("\nEnable Consistency Mode? (yes/no):")
    print("Consistency Mode helps enforce logical continuity in the story to avoid contradictions and plot holes.")
    consistency_input = input("Enter yes or no: ").strip().lower()
    consistency_mode = consistency_input == "yes" 

    print("\nChoose focus mode:")
    print("1. Descriptive - Focus on vivid descriptions and sensory details.")
    print("2. Dialogue - Emphasize character interactions and conversations.")
    print("3. Action - Focus on dynamic scenes and plot progression.")
    print("4. Balanced - Balance description, dialogue, and action.")
    focus_choice = input("Enter 1, 2, 3, or 4: ").strip()
    focus_map = {"1": "descriptive", "2": "dialogue", "3": "action", "4": "balanced"}
    focus_mode = focus_map.get(focus_choice, "balanced")

    if mode_choice == "1":
        # one shot mode
        print("\n[INFO] Generating complete story in one-shot mode...")
        story = generate_one_shot_story(
            caption=caption,
            genre=genre,
            max_words=max_words,
            creativity_level=creativity_level,
            consistency_mode=consistency_mode,
            focus_mode=focus_mode
        )
        
        # completed story
        window, text_widget = setup_window()
        update_window(window, text_widget, story)
        show_completion_message(window)
        
        print("\n[INFO] Story generation complete! Check the UI window.")
        print("Close the UI window when you're done reading.")
        window.mainloop()
        
    else:
        story = interactive_mode(
            caption=caption,
            genre=genre,
            max_words=max_words,
            creativity_level=creativity_level,
            consistency_mode=consistency_mode,
            focus_mode=focus_mode
        )

    title = generate_title(story, genre)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"[TITLE]\n{title}\n\n")
        f.write("[CAPTION]\n")
        f.write(caption + "\n")
        f.write("\n" + "="*30 + "\n\n")
        f.write(f"[STORY] (Genre: {genre})\n")
        f.write(story)

    print(f"\n✅ [INFO] Story saved to {output_file} with Title: {title}")

if __name__ == "__main__":
    main()