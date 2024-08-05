from openai import OpenAI
from dotenv import load_dotenv
import os
from configs.configs import config

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

    try:
        response = client.chat.completions.create(
            model=config.model,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Problems with GPT!")
        raise e
