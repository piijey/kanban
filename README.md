# kanban

2016年〜2026年の間に、関西圏をはじめとする各地で撮影した掲示物（看板・張り紙など）のコレクション。
各写真に、手動で書き起こしたテキストと、メタ情報がついています。

テキスト検索・タグ絞り込みのできる[ビューア (看板コレクション)](https://piijey.github.io/kanban/)を GitHub Pages で公開中。

## データについて

- 画像ファイル: `docs/images/*.JPG`
- メタ情報: `docs/data.json`
  - `signs`: 文字起こしテキスト・ピクトグラム・言語・形態（手動で付与）
  - `date` / `location`: 撮影日・位置（画像のEXIFから取得）
  - `location_info`: `location` を [Nominatim API](https://nominatim.openstreetmap.org/) で逆ジオコーディングした国・都道府県・市区町村など

## ライセンス

- 画像・`signs`・`date`・`location`: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja)（表示: PiiJey）
- `location_info`: [ODbL](https://opendatacommons.org/licenses/odbl/)（[OpenStreetMap](https://www.openstreetmap.org/copyright) のデータ）

## 開発者向け情報

セットアップ・スクリプトの使い方は [DEVELOPMENT.md](DEVELOPMENT.md) を参照。
