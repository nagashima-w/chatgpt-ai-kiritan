import os
import openai
import requests
from google.cloud import speech_v1p1beta1 as speech
from natto import MeCab
from flask import Flask, request, jsonify
from io import BytesIO
from voicevox_engine_wrapper import text_to_speech

app = Flask(__name__)

nm = MeCab()
emotion_dict = {}

with open("pn.csv.m3.120408.trim", "r", encoding="utf-8") as f:
    for line in f:
        word, pos, score = line.strip().split("\t")
        emotion_dict[word] = float(score)

def estimate_emotion_japanese(text):
    tokens = nm.parse(text, as_nodes=True)
    scores = [emotion_dict.get(token.surface, 0) for token in tokens if not token.is_eos()]
    avg_score = sum(scores) / len(scores) if scores else 0
    return "positive" if avg_score > 0 else "negative"

# Google Cloud Speech-to-Text API クライアントのインスタンスを作成
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GCLOUD_KEY_PATH")
client = speech.SpeechClient()

# OpenAI APIキーを設定
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    audio_data = request.files['audio']

    # 音声データをテキストに変換
    text = audio_to_text(client, audio_data)

    # テキストをChatGPTに入力し、返答を取得
    response_text = chat_with_gpt(text)

    # 返答の感情を推定
    emotion = estimate_emotion_japanese(response_text)

    # 返答テキストを音声に変換し、感情を反映させる
    audio_response = text_to_speech(response_text, emotion)

    return jsonify({'audio': audio_response})

def audio_to_text(client, audio_data):
    audio = speech.RecognitionAudio(content=audio_data.read())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ja-JP",
    )

    response = client.recognize(config=config, audio=audio)
    transcript = response.results[0].alternatives[0].transcript
    return transcript

def chat_with_gpt(text):
    model_engine = "text-davinci-002"
    prompt = f"{text}\n\nChatGPT:"

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    response_text = response.choices[0].text.strip()
    return response_text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

