
# 📝 Story Generator

[![Watch the video](https://img.youtube.com/vi/oeUEXCh7mAE/0.jpg)](https://www.youtube.com/watch?v=oeUEXCh7mAE)

A picture is worth a thousand words. Now you can actually see those 1000  or more words.. With this Image to Story generator you can generate stories from images with high editing capabilities.

## Tech Stack

- **Python 3.8+**
- **Tkinter** — Real-time GUI updates.
- **Requests** — For API communication with Ollama Server.
- **Pillow** (optional) — For potential image handling enhancements.
- **Ollama Server** — Local LLM server backend.
- **Models Used**:
  - **qwen2.5vl:7b** — Image Captioning.
  - **llama3.1:8b** — Story and Title Generation.


---

## 🚀 Features
- Generate a story based on a randomly selected image or user-provided image.
- Real-time **Interactive Mode** with live story updates (Tkinter GUI).
- Change genres, add suggestions or change the narrative flow of the story on the fly.
- **One-Shot Mode** for generating the entire story at once and saving it incrementally.
- Generate multiple creative and genre-appropriate **title suggestions**.
- Automatically saves the generated story with a suitable title.
- User can input their own image or let the app select one randomly (Image paths must start with ./images/file_name.extension).

I have added a few images of my own for users to test them. You can add your own images in the images folder for your own ideas and stories.

---

## 📂 What Each File Does

| File/Folder         | Description |
|---------------------|-------------|
| `main.py`            | Main entry point. Runs the app, handles user interaction, and controls flow. |
| `image_caption/`     | Contains `image_caption.py` for generating captions based on input images. |
| `story_gen/`         | Core story generation logic: `story_gen.py` (interactive), `one_shot_gen.py` (one-shot mode), `generate_title.py` (title suggestions), `story_utils.py` (shared utils). |
| `ui/`                | Contains `ui.py` for setting up and updating the Tkinter GUI. |
| `images/`            | Folder to store user images for story generation. |
| `requirements.txt`   | Python dependencies list. |
| `README.md`          | This file — project overview and instructions. |

---

## ⚙️ Installation

```bash
git clone https://github.com/AbhinavChandra7020/image-to-story-testing
cd story-generator
```

**Or Download the zip file and follow the next steps**

Make sure you have **Python 3.8+** installed.

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### 📦 Ollama and Model Setup
You must have [Ollama Server](https://ollama.com/) running locally.

Default Ollama Server API: http://localhost:11434/api/generate

Install the required models via Ollama:

```bash
ollama pull qwen2.5vl:7b
ollama pull llama3.1:8b
```
And then
```bash
ollama run qwen2.5vl:7b
ollama run llama3.1:8b
```
**Note:** You can just start ollama and the models will be automatically called as per requirement. There is no need to run these models simultaneously or open multiple terminals to run them.

> These models are used for:
> - `qwen2.5vl:7b` — Image captioning (vision + language).
> - `llama3.1:8b` — Story generation and title generation.

> **Note:** Make sure the Ollama server is up before running the app.

> **You can either open your terminal and run ollama serve or go to your search bar and start ollama**

---

## 🖥️ Usage

Run the app:

```bash
python main.py
```

You’ll be prompted to:
1. Enter an image path (or leave it blank for random selection).
2. Choose story generation mode:
   
   **1** — One-Shot Mode (full story at once).

   **2** — Interactive Mode (step-by-step updates with suggestions).
3. Set the caption detail level:
   
   **1** — Very Detailed.
   
   **2** — Short Caption.
4. Choose your story genre.
5. Set the maximum word limit (default: 8000 words).

6. Close the "Your Story so Far" window to save the output to the result.txt file and give you options to choose an appropriate title.

The app will:
- Generate a caption for the selected image.
- Generate a story based on the caption and genre.
- Provide 5 creative title options for you to select.
- Save the final story to a `.txt` file with the chosen title.


---



## License

This project is open-sourced under the [MIT License](LICENSE).

---

## Acknowledgements

- [Ollama Server](https://ollama.com/) for local model serving.
- Qwen-2.5 VL for Image Captioning .
- Llama 3.1 models for Story Generation.
- Python and Tkinter for GUI handling.