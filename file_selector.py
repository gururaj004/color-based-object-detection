import tkinter as tk
from tkinter import filedialog


def select_file(file_type):
    root = tk.Tk()
    root.withdraw()

    if file_type == "image":
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp"),
                ("All Files", "*.*")
            ]
        )
    else:
        file_path = filedialog.askopenfilename(
            title="Select a Video",
            filetypes=[
                (
                    "Video Files",
                    "*.mp4 *.avi *.mov *.mkv *.webm *.m4v *.wmv"
                ),
                ("All Files", "*.*")
            ]
        )

    root.destroy()
    return file_path