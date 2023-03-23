import requests
from io import BytesIO
import config

def text_to_speech(text, emotion):
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

    return audio_data

