import tkinter as tk
from tkinter import ttk

def apply_styles(root):
    default_font = ("Arial", 10)
    bold_font = ("Arial", 10, "bold")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=default_font, padding=5)
    style.configure("TLabel", font=default_font)
    style.configure("Treeview.Heading", font=bold_font)
    style.configure("Treeview", font=default_font, rowheight=25)
    style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
    style.map("Treeview", background=[("selected", "#347083")], foreground=[("selected", "white")])

    # 上方按鈕區
    root.frame_top = tk.Frame(root)
    root.frame_top.pack(pady=10, fill=tk.X)
    root.frame_center = tk.Frame(root.frame_top)
    root.frame_center.pack(anchor="center")
    root.frame_buttons = tk.Frame(root.frame_center)
    root.frame_buttons.pack(side=tk.LEFT)
    root.frame_output = tk.Frame(root.frame_center)
    root.frame_output.pack(side=tk.LEFT, padx=20)

    # 表格區
    root.frame_table = tk.Frame(root)
    root.frame_table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    columns = ("資料夾名稱","檔名","原副檔名","輸出副檔名","新尺寸")
    root.table = ttk.Treeview(root.frame_table, columns=columns, show="headings")
    root.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = ttk.Scrollbar(root.frame_table, orient="vertical", command=root.table.yview)
    root.table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    for col in columns:
        root.table.heading(col, text=col)

    def adjust_columns(event=None):
        total_width = root.table.winfo_width()
        if total_width <= 0:
            return
        root.table.column("資料夾名稱", width=int(total_width*0.20))
        root.table.column("檔名", width=int(total_width*0.35))
        root.table.column("原副檔名", width=int(total_width*0.10))
        root.table.column("輸出副檔名", width=int(total_width*0.10))
        root.table.column("新尺寸", width=int(total_width*0.25))
    root.table.bind("<Configure>", adjust_columns)

    # 下方功能區
    root.frame_bottom = tk.Frame(root)
    root.frame_bottom.pack(pady=5, fill=tk.X)
    root.frame_format = tk.Frame(root.frame_bottom)
    root.frame_format.pack(side=tk.LEFT, expand=True)
    root.frame_resize = tk.Frame(root.frame_bottom)
    root.frame_resize.pack(side=tk.RIGHT, expand=True)

    return {"columns": columns, "adjust_columns": adjust_columns}
