import subprocess
from tkinter import messagebox

SUPPORTED_FORMATS = (".png", ".jpg", ".jpeg", ".webp")

def is_supported(file_path):
    return file_path.lower().endswith(SUPPORTED_FORMATS)

def calc_ratio(orig_w, orig_h, target_w=None, target_h=None):
    if target_w and target_h:
        return min(target_w / orig_w, target_h / orig_h)
    elif target_w:
        return target_w / orig_w
    elif target_h:
        return target_h / orig_h
    else:
        return 1

def open_in_explorer(path):
    try:
        subprocess.run(["explorer", "/select,", path.replace("/", "\\")])
    except Exception as e:
        messagebox.showerror("錯誤", f"無法開啟檔案總管:\n{e}")
