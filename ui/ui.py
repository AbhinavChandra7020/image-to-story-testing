import tkinter as tk
from tkinter import scrolledtext, ttk
import tkinter.font as tkFont

def setup_window():
    """
    Sets up the main tkinter window with enhanced visual appeal.
    
    Returns:
        window: The main tkinter window instance.
        text_widget: The text area widget for displaying the story.
    """
    window = tk.Tk()
    window.title("📖 AI Story Generator")
    
    # Set window size and make it resizable
    window.geometry('1200x800')
    window.minsize(800, 600)
    
    # Configure modern color scheme
    bg_color = "#1e1e2e"  # Dark purple-gray
    secondary_bg = "#313244"  # Lighter purple-gray
    accent_color = "#89b4fa"  # Light blue
    text_color = "#cdd6f4"  # Light gray-blue
    highlight_color = "#f38ba8"  # Pink accent
    
    window.configure(bg=bg_color)
    
    # Configure modern style for ttk widgets
    style = ttk.Style()
    style.theme_use('clam')
    
    # Create main container with padding
    main_frame = tk.Frame(window, bg=bg_color)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Header section with gradient-like effect
    header_frame = tk.Frame(main_frame, bg=bg_color, height=80)
    header_frame.pack(fill=tk.X, pady=(0, 20))
    header_frame.pack_propagate(False)
    
    # Title with modern typography
    title_font = tkFont.Font(family="Segoe UI", size=24, weight="bold")
    subtitle_font = tkFont.Font(family="Segoe UI", size=12)
    
    title_label = tk.Label(
        header_frame,
        text="✨ Your Story Unfolds",
        font=title_font,
        bg=bg_color,
        fg=accent_color,
        pady=10
    )
    title_label.pack()
    
    subtitle_label = tk.Label(
        header_frame,
        text="Watch as your AI-generated story comes to life",
        font=subtitle_font,
        bg=bg_color,
        fg=text_color
    )
    subtitle_label.pack()
    
    # Story content frame with modern card-like appearance
    content_frame = tk.Frame(main_frame, bg=secondary_bg, relief=tk.FLAT)
    content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # Add some padding inside the content frame
    inner_frame = tk.Frame(content_frame, bg=secondary_bg)
    inner_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    # Enhanced text widget with better styling
    text_font = tkFont.Font(family="Georgia", size=13, weight="normal")
    
    text_widget = scrolledtext.ScrolledText(
        inner_frame,
        wrap=tk.WORD,
        font=text_font,
        bg="#181825",  # Darker background for text area
        fg=text_color,
        insertbackground=accent_color,
        selectbackground=highlight_color,
        selectforeground="#1e1e2e",
        relief=tk.FLAT,
        borderwidth=0,
        padx=20,
        pady=15,
        spacing1=2,  # Space before paragraphs
        spacing2=1,  # Space between lines in same paragraph
        spacing3=4   # Space after paragraphs
    )
    text_widget.pack(fill=tk.BOTH, expand=True)
    
    # Configure text widget scrollbar styling
    text_widget.vbar.configure(
        bg=secondary_bg,
        troughcolor=secondary_bg,
        activebackground=accent_color,
        width=12
    )
    
    # Status bar at the bottom
    status_frame = tk.Frame(main_frame, bg=bg_color, height=30)
    status_frame.pack(fill=tk.X, pady=(10, 0))
    status_frame.pack_propagate(False)
    
    status_label = tk.Label(
        status_frame,
        text="● Ready to generate your story",
        font=("Segoe UI", 10),
        bg=bg_color,
        fg=accent_color,
        anchor="w"
    )
    status_label.pack(fill=tk.X, padx=5)
    
    # Add some visual polish with separator lines
    separator1 = tk.Frame(main_frame, height=1, bg=accent_color)
    separator1.pack(fill=tk.X, pady=(0, 10))
    
    # Configure grid weights for responsive design
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    
    # Store status label for updates
    window.status_label = status_label
    
    window.update()
    return window, text_widget

def update_window(window, text_widget, new_text):
    """
    Updates the text widget with new story content and adds visual feedback.
    
    Args:
        window: The tkinter window instance.
        text_widget: The scrolled text widget.
        new_text: The new text to display.
    """
    # Clear and update text
    text_widget.delete('1.0', tk.END)
    
    # Add the new text with some formatting
    lines = new_text.split('\n')
    for i, line in enumerate(lines):
        if line.strip():  # Non-empty line
            text_widget.insert(tk.END, line)
        text_widget.insert(tk.END, '\n')
    
    # Auto-scroll to bottom to show latest content
    text_widget.see(tk.END)
    
    # Update status
    word_count = len(new_text.split())
    if hasattr(window, 'status_label'):
        window.status_label.config(text=f"● Story updated • {word_count:,} words")
    
    # Refresh the window
    window.update()
    
    # Add a subtle animation effect by briefly changing the background
    original_bg = text_widget.cget('bg')
    text_widget.configure(bg="#1f1f35")  # Slightly lighter background
    window.after(100, lambda: text_widget.configure(bg=original_bg))

def show_completion_message(window):
    """
    Shows a completion message when the story is finished.
    
    Args:
        window: The tkinter window instance.
    """
    if hasattr(window, 'status_label'):
        window.status_label.config(
            text="✅ Story completed! Your masterpiece is ready.",
            fg="#a6e3a1"  # Green color for completion
        )

def update_status(window, message, color=None):
    """
    Updates the status bar with a custom message.
    
    Args:
        window: The tkinter window instance.
        message: The status message to display.
        color: Optional color for the message.
    """
    if hasattr(window, 'status_label'):
        if color:
            window.status_label.config(text=f"● {message}", fg=color)
        else:
            window.status_label.config(text=f"● {message}")
    window.update()