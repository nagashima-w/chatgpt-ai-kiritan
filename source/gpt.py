import openai
from config import OPENAI_API_KEY

# APIキーを設定
openai.api_key = OPENAI_API_KEY

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

