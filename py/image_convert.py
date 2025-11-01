from PIL import Image
import os

def convert_images(file_list, output_dir, target_format, progress_bar=None, progress_label=None):
    total = len(file_list)
    for i, (full_path, rel_path) in enumerate(file_list, 1):
        try:
            img = Image.open(full_path).convert("RGB")
            save_dir = os.path.join(output_dir, rel_path) if rel_path else output_dir
            os.makedirs(save_dir, exist_ok=True)
            name = os.path.splitext(os.path.basename(full_path))[0]
            save_path = os.path.join(save_dir, f"{name}.{target_format.lower()}")
            img.save(save_path, target_format.upper())
        except Exception as e:
            print(f"轉換失敗: {full_path} -> {e}")

        if progress_bar is not None:
            progress_bar["value"] = (i / total) * 100
            progress_bar.update()
        if progress_label is not None:
            progress_label.config(text=f"{i}/{total}")
            progress_label.update()
