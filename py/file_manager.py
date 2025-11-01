import os
from tkinter import filedialog

file_list = []  # [(full_path, relative_path)]

def add_files():
    files = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp")])
    for f in files:
        if f not in [x[0] for x in file_list]:
            file_list.append((f, ""))

def add_folder():
    folder = filedialog.askdirectory()
    if folder:
        for root_dir, _, files in os.walk(folder):
            for f in files:
                if f.lower().endswith((".png",".jpg",".jpeg",".webp")):
                    full_path = os.path.join(root_dir,f)
                    rel_path = os.path.relpath(root_dir, folder)
                    file_list.append((full_path, rel_path))

def remove_files(indices):
    global file_list
    for index in sorted(indices, reverse=True):
        if 0 <= index < len(file_list):
            del file_list[index]
