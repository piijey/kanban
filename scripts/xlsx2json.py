#!/usr/bin/env python3
"""
Excel から JSON への変換スクリプト
data_excel/*.xlsx → docs/data.json
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Any, Optional
import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS


def get_image_metadata(image_path: str) -> dict:
    """
    画像ファイルから EXIF データを取得
    date: 撮影日時 (ISO 8601形式)
    location: 緯度・経度
    """
    result = {"date": None, "location": None}
    
    if not os.path.exists(image_path):
        return result
    
    try:
        image = Image.open(image_path)        
        exif_data = image._getexif()
        
        if exif_data:
            # DateTime (tag 306)
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if tag_name == "DateTime":
                    # Format: "2024:03:15 14:30:00" → ISO 8601
                    dt = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                    result["date"] = dt.isoformat()
                    break
            
            # GPS情報 (tag 34853 GPSInfo)
            if 34853 in exif_data:
                gps_info = exif_data[34853]
                lat = convert_gps_to_decimal(gps_info.get(2))
                lng = convert_gps_to_decimal(gps_info.get(4))
                lat_ref = gps_info.get(1)  # "N" or "S"
                lng_ref = gps_info.get(3)  # "E" or "W"
                
                if lat and lng:
                    if lat_ref == "S":
                        lat = -lat
                    if lng_ref == "W":
                        lng = -lng
                    result["location"] = {"lat": round(lat, 4), "lng": round(lng, 4)}
    except Exception as e:
        print(f"Warning: Could not read EXIF from {image_path}: {e}")

    return result


def convert_gps_to_decimal(gps_tuple: Optional[Any]) -> Optional[float]:
    """
    GPS座標をタプル形式から小数形式に変換
    (度, 分, 秒) → 度数法
    """
    if not gps_tuple:
        return None
    try:
        d, m, s = gps_tuple
        # gps_tuple は (度, 分, 秒) の float タプル
        return float(d) + float(m) / 60 + float(s) / 3600
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def split_pipe_separated(value: Any) -> list:
    """
    | で区切られた文字列をリストに分割
    None や "None" の場合は空リストを返す
    """
    if value is None or value == "None" or (isinstance(value, float) and pd.isna(value)):
        return []
    return [v.strip() for v in str(value).split("|") if v.strip()]


def excel_to_json(excel_path: str, output_path: str, images_dir: str) -> None:
    """
    Excel ファイルを JSON に変換
    """
    # Excelを読み込む
    df = pd.read_excel(excel_path)
    
    # 必要なカラムの確認
    required_cols = {"img", "sign_idx", "text", "pictograms", "language", "form", "notes"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Required columns missing: {required_cols - set(df.columns)}")
    
    # img ごとにグルーピング
    grouped = df.groupby("img", sort=False)
    result = []
    
    for img_name, group in grouped:
        # id と image パスの生成
        img_id = Path(img_name).stem  # 拡張子を除いたファイル名
        normalized_img_name = img_id + '.JPG'  # 変換済みJPGファイル名
        image_path = os.path.join(images_dir, normalized_img_name)
        
        # EXIF情報の取得
        metadata = get_image_metadata(image_path)
        
        # signs配列の構築
        signs = []
        
        for _, row in group.iterrows():
            sign = {
                "text": str(row["text"]),
                "pictograms": split_pipe_separated(row.get("pictograms")),
                "language": split_pipe_separated(row.get("language")),
                "form": split_pipe_separated(row.get("form")),
            }
            signs.append(sign)
        
        # 1レコード構築
        record = {
            "id": img_id,
            "image": f"images/{normalized_img_name}",
            "signs": signs,
            "date": metadata["date"],
            "location": metadata["location"],
            "original_image": img_name,
            "notes": str(group["notes"].dropna().iloc[0]) if not group["notes"].dropna().empty else None,
            "link": str(group["link"].dropna().iloc[0]) if not group["link"].dropna().empty else None
        }
        result.append(record)

        if metadata["date"] is None or metadata["location"] is None:
            print(f" ▲ Note: Missing metadata for {image_path}:\n   date={metadata['date']}, location={metadata['location']}")
    
    # JSON出力
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Generated {output_path} ({len(result)} records)")


if __name__ == "__main__":
    # ファイルパスの設定
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    
    excel_file = project_dir / "data_excel" / "tags.xlsx"
    output_file = project_dir / "docs" / "data.json"
    images_dir = project_dir / "docs" / "images"  # 変換済みJPGから読む
    
    if not excel_file.exists():
        print(f"Error: Excel file not found: {excel_file}")
        exit(1)
    
    excel_to_json(str(excel_file), str(output_file), str(images_dir))
