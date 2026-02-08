# Yo!

わからないことがあったら気軽に質問してね。

- 開発環境の構築には mamba を使用します。
```sh
mamba activate env-kanban-corpus
```

- やりたいことは `kanban-corpus-spec.md` を参照。


---

## 課題　(issues)
### 一部の画像で撮影日時　(date)・位置情報 (location) の変換に失敗している
#### 【現状】
1. 最初：data_raw-img/ から直接EXIF読み込み
   → HEICはPillow非対応、JPGは読めた
2. 改善試行：HEICをJPGに変換
   → 変換後JPGから位置情報取得しようとした
3. 問題：pillow-heifでHEIC→JPGに変換すると、EXIFが失われる
   → HEICのEXIFをpillow-heifで抽出できない（APIの制限）
4. 現状の結果：
   - 元JPG：位置情報 ✅
   - HEIC→JPG：位置情報 ❌

#### 【打ち手の選択肢】
A. HEICの位置情報を Excelで手動入力  
B. piexif/exifread で直接HEIC EXIFを抽出（実装難度高）  
C. 元のHEIC ファイルもdist/に保持して、両方から読む  
D. ImageMagickやffmpegなど別ツール使用


### GitHub Pages リポジトリ設定
- GitHub → Settings → Pages
- Source: Deploy from a branch
- Branch: main / Folder: dist
- 保存
