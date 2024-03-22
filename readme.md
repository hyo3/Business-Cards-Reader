# OCR_NAME_CARD

- 写真を撮って送るとスプレッドシートに登録してくれる LINE Bot のソースです

## 実行環境

- Python 3.12.2
- venv
- その他`requirements.txt`に記載

## 構成

### サーバー `main.py`

- FastAPI

### OCR `vision_api.py`

- GCP cloud vision API
  - 認証するための JSON は base64 エンコードして環境変数に設定

### 項目の分割 `create_chat.py`

- OPENAI API `gpt-4-turbo-preview` の JSON モードを利用
- 一時的に`gpt-3.5-turbo-0125`を使用

### データベース `post_stein.py`

- スプレッドシートを利用
- [Stein](https://steinhq.com/)を利用して API 化
- API エンドポイントは環境変数に設定

### LINE Bot `line_handler.py`

- LINE 経由でのリクエストに対する処理を記述

### レコメンド

- embeddingで職業をベクトル化
- numpyを利用してコサイン類似度を計算

### 環境変数

- GCP_JSON_STR
- LINE_CHANNEL_ACCESS_TOKEN
- LINE_CHANNEL_SECRET
- OPENAI_API_KEY
- STEIN_URL
- STEIN_URL_EMB

### ホスティング先

- [Render](https://render.com/)

### デプロイ

- bitbucket を使ったデプロイが難しそうだったので、github にリポジトリを作成
- Render と github と紐づけ
- 各種環境変数の設定と Vision API の json ファイルの設定
- Render で発行した URL(https://business-cards-reader.onrender.com)でLINE Developer の設定

## その他ファイル

### `encoder.py`

- base64 エンコード時に利用
