import io
import pyaudio
import requests
from config import GCLOUD_KEY_PATH, VOICEVOX_API_URL, SPEAKER_ID
from google.cloud import texttospeech, speech_v1p1beta1 as speech
from google.oauth2 import service_account
from gpt import chat_with_gpt

credentials = service_account.Credentials.from_service_account_file(GCLOUD_KEY_PATH)

tts_client = texttospeech.TextToSpeechClient(credentials=credentials)
stt_client = speech.SpeechClient(credentials=credentials)

def record_audio():
    audio_format = pyaudio.paInt16
    sample_rate = 16000
    channels = 1
    chunk_size = 1024
    audio = pyaudio.PyAudio()

    stream = audio.open(format=audio_format,
                        rate=sample_rate,
                        channels=channels,
                        input=True,
                        frames_per_buffer=chunk_size)

    print("録音を開始してください。")
    frames = []

    for _ in range(0, int(sample_rate / chunk_size * 5)):
        data = stream.read(chunk_size)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    return b''.join(frames)

def speech_to_text(audio_data):
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ja-JP"
    )

    response = stt_client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript if response.results else ""

def text_to_speech(text):
    response = requests.post(
        f"{VOICEVOX_API_URL}/audio_query",
        json={
            "text": text,
            "speaker": SPEAKER_ID,
            "speedScale": 1.0,
            "pitchScale": 0.0,
            "intonationScale": 1.0,
            "volumeScale": 1.0,
        },
    )

    audio_query = response.json()
    response = requests.post(f"{VOICEVOX_API_URL}/synthesis", json=audio_query)
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

def main():
    while True:
        audio_data = record_audio()
        text = speech_to_text(audio_data)
        print(f"あなた: {text}")

        response_text = chat_with_gpt(text)
        print(f"ChatGPT: {response_text}")

        text_to_speech(response_text)

if __name__ == "__main__":
    main()

