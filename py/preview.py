import tkinter as tk
from PIL import Image, ImageTk
import os
import textwrap

class PreviewWindow:
    def __init__(self, file_list, index, master=None, main_width=950):
        self.file_list = file_list
        self.index = index
        self.top = tk.Toplevel(master)
        self.top.title("圖片預覽")
        self.top.geometry(f"{main_width}x600")  # 與主界面同寬

        # 左右框架
        self.frame_left = tk.Frame(self.top)
        self.frame_left.pack(side=tk.LEFT, padx=10, pady=10)
        self.frame_right = tk.Frame(self.top)
        self.frame_right.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # 左側圖片
        self.label_img = tk.Label(self.frame_left)
        self.label_img.pack()

        # 右側資訊框架（屬性 + 值）
        self.info_frame = tk.Frame(self.frame_right)
        self.info_frame.pack(fill=tk.BOTH, expand=True)

        # 按鈕區（同一行）
        self.btn_frame = tk.Frame(self.frame_right)
        self.btn_frame.pack(pady=10)
        tk.Button(self.btn_frame, text="上一張", width=12, command=self.prev_image).pack(side=tk.LEFT, padx=5)
        tk.Button(self.btn_frame, text="下一張", width=12, command=self.next_image).pack(side=tk.LEFT, padx=5)

        self.show_image()

    def show_image(self):
        path = self.file_list[self.index]
        img = Image.open(path)
        img.thumbnail((500, 500))
        self.photo = ImageTk.PhotoImage(img)
        self.label_img.config(image=self.photo)
        self.label_img.image = self.photo

        # 清空右側資訊
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        w, h = img.size
        size_kb = os.path.getsize(path) / 1024
        ext = os.path.splitext(path)[1].lower()
        full_path = os.path.abspath(path)

        info_list = [
            ("檔案路徑", full_path),
            ("寬 × 高", f"{w} × {h}"),
            ("檔案大小", f"{size_kb:.2f} KB"),
            ("副檔名 / 格式", ext),
            ("索引", f"{self.index+1}/{len(self.file_list)}")
        ]

        # 設定屬性欄寬度
        attr_width = 12  # 字元寬度，可調整
        wrap_chars = 60  # 值欄換行寬度

        for attr, val in info_list:
            frame = tk.Frame(self.info_frame)
            frame.pack(fill=tk.X, pady=2, anchor="w")

            label_attr = tk.Label(frame, text=attr, width=attr_width, anchor="w", font=("Arial", 10, "bold"))
            label_attr.pack(side=tk.LEFT)

            # 值欄自動換行
            wrapped_val = "\n".join(textwrap.wrap(val, width=wrap_chars))
            label_val = tk.Label(frame, text=wrapped_val, anchor="w", justify="left", font=("Arial", 10))
            label_val.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.top.title(f"圖片預覽 ({self.index+1}/{len(self.file_list)})")

    def prev_image(self):
        if self.index > 0:
            self.index -= 1
            self.show_image()

    def next_image(self):
        if self.index < len(self.file_list) - 1:
            self.index += 1
            self.show_image()

def open_preview_window(file_list, index, master=None, main_width=950):
    PreviewWindow(file_list, index, master, main_width)
