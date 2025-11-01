import os
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image
import file_manager, image_convert, image_resize, preview
import style

root = tk.Tk()
root.title("🖼️ 圖片批量處理器 v9.6")
root.geometry("950x700")
root.resizable(True, True)

file_list = file_manager.file_list
output_path = tk.StringVar()
format_var = tk.StringVar()

style_dict = style.apply_styles(root)
table = root.table
frame_buttons = root.frame_buttons
frame_output = root.frame_output
frame_format = root.frame_format
frame_resize = root.frame_resize

# ===== 上方按鈕 =====
tk.Button(frame_buttons, text="選擇檔案", width=12,
          command=lambda:[file_manager.add_files(), update_table()]).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="選擇資料夾", width=12,
          command=lambda:[file_manager.add_folder(), update_table()]).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="移除選取", width=12,
          command=lambda:[file_manager.remove_files([table.index(i) for i in table.selection()]), update_table()]).pack(side=tk.LEFT, padx=5)

tk.Label(frame_output, text="輸出資料夾：").pack(side=tk.LEFT)
tk.Entry(frame_output, textvariable=output_path, width=50).pack(side=tk.LEFT, padx=5)
tk.Button(frame_output, text="選擇", command=lambda: output_path.set(filedialog.askdirectory())).pack(side=tk.LEFT)

lbl_count = tk.Label(root, text="尚未選擇檔案")
lbl_count.pack()

# ===== 更新表格 =====
def update_table():
    table.delete(*table.get_children())
    target_format = format_var.get().lower()
    
    target_w = int(entry_width.get()) if entry_width.get() else None
    target_h = int(entry_height.get()) if entry_height.get() else None

    for full_path, rel_path in file_list:
        folder_name = rel_path if rel_path else os.path.basename(os.path.dirname(full_path))
        name = os.path.splitext(os.path.basename(full_path))[0]
        ext = os.path.splitext(full_path)[1].lower()
        new_ext = f".{target_format}" if target_format else ""

        img = Image.open(full_path)
        w, h = img.size
        if target_w and target_h:
            new_w, new_h = target_w, target_h
        elif target_w:
            new_w = target_w
            new_h = int(h * target_w / w)
        elif target_h:
            new_h = target_h
            new_w = int(w * target_h / h)
        else:
            new_w, new_h = w, h

        size_str = f"{new_w}×{new_h}"
        table.insert("", tk.END, values=(folder_name, name, ext, new_ext, size_str))
    
    lbl_count.config(text=f"共選擇 {len(file_list)} 個檔案")

# ===== 表格雙擊預覽 =====
def on_double_click(event):
    selection = table.selection()
    if selection:
        index = table.index(selection[0])
        preview.open_preview_window([f for f,_ in file_list], index, root)
table.bind("<Double-1>", on_double_click)

# ===== 統一進度條（無文字） =====
progress_global = ttk.Progressbar(root, length=750, mode="determinate")
progress_global.pack(pady=10)

# ===== 格式轉換區 =====
tk.Label(frame_format, text="格式轉換區").pack(anchor="center", pady=2)
frame_format_inner = tk.Frame(frame_format)
frame_format_inner.pack(anchor="center")

combo = ttk.Combobox(frame_format_inner, textvariable=format_var,
                     values=["png","jpg","jpeg","webp"], width=10, state="readonly")
combo.pack(side=tk.LEFT, padx=5)
combo.bind("<<ComboboxSelected>>", lambda e: update_table())

tk.Button(frame_format_inner, text="開始轉換",
          command=lambda: image_convert.convert_images(file_list, output_path.get(), format_var.get(), progress_global, None)).pack(side=tk.LEFT, padx=5)

# ===== 尺寸修改區 =====
tk.Label(frame_resize,text="尺寸修改區（保持比例）").pack(anchor="center")
tk.Label(frame_resize,text="寬(px)").pack(side=tk.LEFT,padx=5)
entry_width = tk.Entry(frame_resize,width=6)
entry_width.pack(side=tk.LEFT,padx=5)
tk.Label(frame_resize,text="高(px)").pack(side=tk.LEFT,padx=5)
entry_height = tk.Entry(frame_resize,width=6)
entry_height.pack(side=tk.LEFT,padx=5)

entry_width.bind("<KeyRelease>", lambda e: update_table())
entry_height.bind("<KeyRelease>", lambda e: update_table())

tk.Button(frame_resize,text="批量修改尺寸",
          command=lambda: image_resize.resize_images(
              file_list, output_path.get(),
              int(entry_width.get()) if entry_width.get() else None,
              int(entry_height.get()) if entry_height.get() else None,
              progress_global, None
          )).pack(side=tk.LEFT,padx=5)

root.mainloop()
