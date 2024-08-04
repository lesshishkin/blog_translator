from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv('.env')
API_KEY = os.environ['GPT_API_KEY']


def ask_gpt(prompt, text=None):
    if text is not None:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    else:
        messages = [
            {"role": "system", "content": prompt},
        ]

    client = OpenAI(api_key=API_KEY)
    translation = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    # todo check it
    return translation['choices'][0]['message']['content']