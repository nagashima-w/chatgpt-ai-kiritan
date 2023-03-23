このREADMEはChatGPTに生成させました。

# ChatGPT with VOICEVOX Engine

このアプリケーションでは、音声を入力して、OpenAIのChatGPTを使って会話し、VOICEVOX Engineを使って音声出力を行うことができます。

## 必要なもの

- Docker
- Docker Compose
- Google Cloud APIキー (Speech-to-Textを利用するため)
- OpenAI APIキー

## セットアップ

1. このリポジトリをクローンします。

```bash
git clone https://github.com/yourusername/chatgpt-voicevox.git
cd chatgpt-voicevox
```


2. 必要な環境変数を設定します。以下のコマンドを実行し、環境変数を設定した`.env`ファイルを作成します。各環境変数に適切な値を設定してください。

```bash
cp .env.example .env
```


3. Dockerイメージをビルドし、コンテナを起動します。

```bash
docker-compose build
docker-compose up -d
```


## 使用方法

1. ブラウザを開き、`http://localhost:8000`にアクセスします。

2. 音声入力ボタンをクリックし、マイクを使って話しかけます。

3. 音声がテキストに変換され、ChatGPTによって返答が生成されます。

4. 返答が音声に変換され、AIきりたんの声で聞くことができます。

## 設定

環境変数を使って、アプリケーションの設定を変更することができます。以下に設定可能な環境変数を示します。

- `OPENAI_API_KEY`: OpenAI APIキー
- `GCLOUD_KEY_PATH`: Google Cloud APIキーのパス
- `VOICEVOX_API_URL`: VOICEVOX EngineのAPI URL
- `SPEAKER_ID`: AIきりたんのID (0: 京町セイカ, 1: 四国めたん)

これらの環境変数は、`.env`ファイルに設定することができます。`.env`ファイルが存在しない場合は、.env.exampleファイルをコピーして使用してください。



