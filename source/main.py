import openai
import requests
import pyaudio
from natto import MeCab
import config

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

def text_to_speech(text):
    emotion = estimate_emotion_japanese(text)

    speed_scale = 1.0
    pitch_scale = 0.0
    intonation_scale = 1.0

    if emotion == "positive":
        speed_scale = 1.2
        pitch_scale = 0.5
        intonation_scale = 1.2
    elif emotion == "negative":
        speed_scale = 0.9
        pitch_scale = -0.5
        intonation_scale = 0.8

    response = requests.post(
        f"{config.VOICEVOX_API_URL}/audio_query",
        json={
            "text": text,
            "speaker": config.SPEAKER_ID,
            "speedScale": speed_scale,
            "pitchScale": pitch_scale,
            "intonationScale": intonation_scale,
            "volumeScale": 1.0,
        },
    )

    audio_query = response.json()
    response = requests.post(f"{config.VOICEVOX_API_URL}/synthesis", json=audio_query)
    audio_data = response.content

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=audio.get_format_from_width(2),
        channels=1,
        rate=24000,
        output=True,
    )

    stream.write(audio_data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

if __name__ == "__main__":
    while True:
        text = input("あなた: ")
        response_text = chat_with_gpt(text)
        print("ChatGPT:", response_text)
        text_to_speech(response_text)
