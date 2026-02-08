#!/usr/bin/env python3
"""
全ての画像をdocs/imagesにコピー＆リサイズ＆最適化
- HEIC/JPG/PNG → JPG統一
仕様: 長辺1600px、品質85から調整、目標1MB以下

Usage:
    python convert_heic_to_jpg.py          # 既存ファイルをスキップ
    python convert_heic_to_jpg.py --force  # 全ファイルを処理
"""

import os
import sys
from pathlib import Path
from PIL import Image
import pillow_heif

# HEIC 対応を登録
pillow_heif.register_heif_opener()


def process_image(input_path: str, output_path: str, target_size_mb: float = 1.0) -> None:
    """画像をリサイズ＆最適化してJPGで保存"""
    
    # 画像を読み込み（HEIC も JPG も同じ方法）
    image = Image.open(input_path)
    exif = image.getexif()

    # デバッグ用に EXIF 情報を表示
    if 34853 in exif:
        pass
    else:
        print(f"  No GPS EXIF data in {input_path}:\n    {exif}")
        
    # RGB に変換
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # リサイズ（長辺1600px）
    max_width = 1600
    width, height = image.size
    if max(width, height) > max_width:
        ratio = max_width / max(width, height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # 品質調整ループ
    target_size_kb = target_size_mb * 1024
    quality = 85
    
    while quality >= 40:
        image.save(output_path, 'JPEG', quality=quality, optimize=True, exif=exif)
        file_size_kb = os.path.getsize(output_path) / 1024
        
        if file_size_kb <= target_size_kb:
            print(f"✓ {Path(input_path).name:20} → {Path(output_path).name:20} ({file_size_kb:.0f}KB, Q{quality})")
            return
        
        quality -= 5


def main():
    # コマンドライン引数処理
    force_process = '--force' in sys.argv
    
    project_dir = Path(__file__).parent.parent
    images_dir = project_dir / "data_raw-img"
    output_dir = project_dir / "docs" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 全ての画像ファイルを収集
    image_files = sorted([
        p for p in images_dir.glob("*")
        if p.suffix.lower() in ['.heic', '.heif', '.jpg', '.jpeg', '.png']
    ])
    
    if not image_files:
        print("No image files found.")
        return
    
    # 処理対象のファイルをフィルタ
    files_to_process = []
    for img_path in image_files:
        output_path = output_dir / img_path.with_suffix(".JPG").name
        
        if output_path.exists() and not force_process:
            # スキップ
            continue
        
        files_to_process.append((img_path, output_path))
    
    if not files_to_process:
        print("All images are already processed. Use '--force' to reprocess all files.")
        return
    
    print(f"Processing {len(files_to_process)} images...\n")
    
    for img_path, output_path in files_to_process:
        try:
            process_image(str(img_path), str(output_path))
        except Exception as e:
            print(f"✗ Error processing {img_path.name}: {e}")
    
    print(f"\n✓ Complete! Total {len(files_to_process)} images processed in {output_dir}")


if __name__ == "__main__":
    main()
