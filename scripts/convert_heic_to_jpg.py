#!/usr/bin/env python3
"""
全ての画像をdist/imagesにコピー＆リサイズ＆最適化
- HEIC → JPG変換
- JPG/PNG → リサイズ＆最適化
仕様: 長辺1600px、品質85から調整、目標1MB以下、全てJPG統一
"""

import os
from pathlib import Path
from PIL import Image, ImageOps
import pillow_heif


def process_image(input_path: str, output_path: str, target_size_mb: float = 1.0) -> None:
    """
    画像をリサイズ＆最適化してJPGで保存
    HEIC/JPG/PNG すべて統一処理
    
    Args:
        input_path: 入力ファイルパス
        output_path: 出力JPGファイルパス
        target_size_mb: 目標ファイルサイズ（MB）
    """
    # 画像を読み込み
    if input_path.lower().endswith(('.heic', '.heif')):
        # HEICは ffmpeg で自動回転付きで読み込むのが確実
        # 一時ファイルに変換
        import tempfile
        import subprocess
        
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # ffmpeg で自動回転を適用しながら変換
            subprocess.run(
                ['ffmpeg', '-i', input_path, '-vf', 'transpose=2,transpose=2', '-q:v', '2', tmp_path],
                capture_output=True,
                timeout=30
            )
            image = Image.open(tmp_path)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            # ffmpeg がない場合は pillow-heif に頼る
            heif_file = pillow_heif.read_heif(input_path)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                'raw',
                heif_file.mode,
                heif_file.stride,
            )
        finally:
            import os as os_mod
            try:
                os_mod.remove(tmp_path)
            except:
                pass
    else:
        image = Image.open(input_path)
    
    # EXIF Orientation を先に適用
    try:
        image = ImageOps.exif_transpose(image)
    except Exception as e:
        pass
    
    # EXIFを取得・保持（ただし Orientation タグは削除）
    exif_data = None
    try:
        exif_data = image.info.get('exif')
        if not exif_data and hasattr(image, '_getexif'):
            raw_exif = image._getexif()
            if raw_exif:
                import piexif
                exif_bytes = piexif.Exif()
                for tag, value in raw_exif.items():
                    # Orientation タグ（274）を除外
                    if tag != 274:
                        try:
                            exif_bytes[tag] = value
                        except:
                            pass
                exif_data = exif_bytes.tobytes()
    except Exception as e:
        pass
    
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
    
    # JPGで出力、品質を調整
    target_size_kb = target_size_mb * 1024
    quality = 85
    
    while quality > 40:
        save_kwargs = {'format': 'JPEG', 'quality': quality, 'optimize': True}
        if exif_data:
            save_kwargs['exif'] = exif_data
        
        image.save(output_path, **save_kwargs)
        file_size_kb = os.path.getsize(output_path) / 1024
        
        if file_size_kb <= target_size_kb:
            print(f"✓ {Path(input_path).name:20} → {Path(output_path).name:20} ({file_size_kb:.0f}KB, Q{quality})")
            return
        
        quality -= 5
    
    # 最後の手段
    save_kwargs = {'format': 'JPEG', 'quality': 40, 'optimize': True}
    if exif_data:
        save_kwargs['exif'] = exif_data
    
    image.save(output_path, **save_kwargs)
    file_size_kb = os.path.getsize(output_path) / 1024
    print(f"✓ {Path(input_path).name:20} → {Path(output_path).name:20} ({file_size_kb:.0f}KB, Q40)")


def main():
    project_dir = Path(__file__).parent.parent
    images_dir = project_dir / "data_raw-img"
    dist_images_dir = project_dir / "dist" / "images"
    
    # dist/images ディレクトリを作成
    dist_images_dir.mkdir(parents=True, exist_ok=True)
    
    # 全ての画像ファイルを収集（HEIC/JPG/PNG）
    image_files = []
    for ext in ["*.HEIC", "*.heic", "*.JPG", "*.jpg", "*.PNG", "*.png"]:
        image_files.extend(images_dir.glob(ext))
    
    if not image_files:
        print("No image files found.")
        return
    
    print(f"Processing {len(image_files)} images...\n")
    
    for img_path in sorted(image_files):
        # 出力ファイル名（全てJPGに統一）
        output_path = dist_images_dir / img_path.with_suffix(".JPG").name
        
        try:
            process_image(str(img_path), str(output_path))
        except Exception as e:
            print(f"✗ Error processing {img_path.name}: {e}")
    
    print(f"\n✓ Complete! Total {len(image_files)} images in {dist_images_dir}")


if __name__ == "__main__":
    main()
