from PIL import Image
import os

def resize_images(file_list, output_dir, target_w=None, target_h=None, progress_bar=None, progress_label=None):
    total = len(file_list)
    for i, (full_path, rel_path) in enumerate(file_list, 1):
        try:
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

            img = img.resize((new_w, new_h), Image.LANCZOS)
            save_dir = os.path.join(output_dir, rel_path) if rel_path else output_dir
            os.makedirs(save_dir, exist_ok=True)
            name, ext = os.path.splitext(os.path.basename(full_path))
            save_path = os.path.join(save_dir, f"{name}{ext}")
            img.save(save_path)
        except Exception as e:
            print(f"修改尺寸失敗: {full_path} -> {e}")

        if progress_bar is not None:
            progress_bar["value"] = (i / total) * 100
            progress_bar.update()
        if progress_label is not None:
            progress_label.config(text=f"{i}/{total}")
            progress_label.update()
