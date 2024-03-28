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

- embedding で職業をベクトル化
- numpy を利用してコサイン類似度を計算

### 環境変数

.env ファイルをプロジェクトのルートディレクトリに置き、以下の項目を設定してください。

- GCP_JSON_STR (gcp のキーを含んだ json ファイルを encoder.py でエンコードしたもの)
- LINE_CHANNEL_ACCESS_TOKEN
- LINE_CHANNEL_SECRET
- OPENAI_API_KEY
- STEIN_URL
- （STEIN_URL_EMB）

## セットアップ

コードをクローンし、ルートディレクトリに移動。<br>
仮想環境を以下のコマンドで作成する。

```
python -m venv .venv
```

仮想環境に入る

```
.venv\Scripts\activate
```

依存関係のインストール

```
pip install requirements.txt
```

## ローカルで起動させる方法

参考<br>
https://qiita.com/__jay/items/1e79f105e26e68507f51<br>
https://qiita.com/nanato12/items/4b735b4d95abf2fdb554<br>

1. LINE bot のテスト用チャネルを作成<br>
   [Messaging API 公式サイト](https://developers.line.biz/ja/docs/messaging-api/getting-started/)の「1. LINE Developers コンソールでチャネルを作成する」の手順でチャネルを作成する 。チャネル作成後、チャネル基本設定に記載されているチャネルシークレットと作成したチャネルアクセストークンをメモしておく<br>
   Messaging API 設定 から「応答メッセージ」と「あいさつメッセージ」の編集を開き、設定を無効にする
2. 環境ファイル（.env）ファイル作成 <br>
3. `uvicorn main:app --reload`でローカルで立ち上げる<br>
   `http://127.0.0.1:8000/docs`で api ドキュメントが作成される。
4. ngrok の導入、設定<br>
   [公式サイト](https://dashboard.ngrok.com/)からユーザ登録、ngrok のダウンロード。<br>
   `ngrok.exe` を開き、ngrok 公式サイトの login 後の画面にある「2. Connect your account」に記載されている`ngrok config add-authtoken <YOUR AUTHTOKEN>`をコピー<br>
5. 外部に公開（line の webhook に登録するため）<br>
   `ngrok http 8000` を実行し、ngrok を使って外部に公開する
6. LINE Developers コンソールの Messaging API 設定 > Webhook 設定 にある Webhook URL に`< ngrok の url>/ callback` を入力
7. 「検証」をクリックして、「成功」と表示されれば OK
8. 自分の LINE で LINE Developers コンソールの Messaging API 設定 > ボット情報 にある QR コードから作成した LINE bot を友達追加する

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
