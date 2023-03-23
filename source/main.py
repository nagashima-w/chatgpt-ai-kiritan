import openai
import requests
import pyaudio
from textblob import TextBlob
import config

def estimate_emotion(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    return "positive" if polarity > 0 else "negative"

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
    emotion = estimate_emotion(text)

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
