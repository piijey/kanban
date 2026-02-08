# kanban

## 使い方

### 環境セットアップ

```sh
mamba activate env-kanban-corpus
```

### 開発フロー

1. **画像を用意　＆ Excelでアノテーション**
   - `data_raw-img/` に撮影した写真を追加
   - `data_excel/tags.xlsx` を編集
   - 列: `img`, `sign_idx`, `text`, `pictograms`, `language`, `form`


2. **画像処理**（Excelを編集したときのみ）
   ```sh
   python scripts/convert_heic_to_jpg.py
   ```
   - `data_raw-img/` の HEIC/JPG を最適化
   - リサイズ（長辺1600px）＆品質調整
   - `docs/images/` に JPG で出力

3. **JSON生成**
   ```sh
   python scripts/xlsx2json.py
   ```
   - `data_excel/tags.xlsx` → `docs/data.json`

4. **ローカルプレビュー**
   ```sh
   cd docs && python -m http.server 8000
   ```
   - ブラウザで `http://localhost:8000` にアクセス

### GitHub Pages へのデプロイ

```sh
# 変更をgit化
git add .
git commit -m "Update corpus data and images"
git push origin main
```

- Settings → Pages → Source: `main / /docs`
- 数秒で `https://username.github.io/kanban-corpus/` に公開

## プロジェクト構成

```
/
├── data_excel/             # アノテーション作業用
│   └── tags.xlsx
├── data_raw-img/           # 元画像（リポジにコミットしない）
│   ├── IMG_*.JPG
│   └── IMG_*.HEIC
├── scripts/
│   ├── xlsx2json.py        # Excel→JSON変換
│   └── convert_heic_to_jpg.py  # 画像最適化
├── docs/                   # GitHub Pages公開フォルダ
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   ├── data.json
│   └── images/
├── README.md
├── AGENTS.md  # 残課題など
└── .gitignore
```

## よくある操作

| 操作 | コマンド |
|------|---------|
| データを更新してプレビュー確認 | `python scripts/convert_heic_to_jpg.py && python scripts/xlsx2json.py && cd docs && python -m http.server 8000` |
| ブラウザキャッシュをクリア | Chrome/Firefox: Cmd+Shift+R / Safari: Cmd+Option+R |
| 既存プロセスを終了 | `lsof -i :8000` <br/> `kill -9 <PID>`|
