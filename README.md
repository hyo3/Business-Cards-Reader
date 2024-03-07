## 前提条件
python 3.12.0

任意のディレクトリにクローン、
ルートディレクトリに移動
## 仮想環境の作成

```
python -m venv .venv
```

### 仮想環境に入る

powershell の場合は

```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

を実行後、

```
.venv\Scripts\activate
```

Linux,WSLの場合は
```
surce  .venv/bin/activate
```


を実行。<br>
プロンプトの先頭に (.venv) と表示されれば、仮想環境で実行中です。<br>

### 仮想環境から出る

```
deactivate
```

## ライブラリのインストール

仮想環境に入った後、以下のコマンドを実行

```
pip install -r requirements.txt
```

## 実行
```
uvicorn main:app --reload
```
`http://127.0.0.1:8000/` でブラウザから確認可能

## APIドキュメント

`http://127.0.0.1:8000/docs` で自動生成されたドキュメントを確認できます
