from openai import OpenAI
from configs.configs import config


def ask_gpt(prompt,
            api_key,
            text=None,
            response_format=None):

    if text is not None:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    else:
        messages = [
            {"role": "system", "content": prompt},
        ]

    client = OpenAI(api_key=api_key)

    if response_format is not None:
        # если надо получить json в ответ
        try:
            response = client.beta.chat.completions.parse(
                model=config.model_enhancer,
                messages=messages,
                response_format=response_format,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Problems with GPT!")
            raise e
    else:
        try:
            response = client.chat.completions.create(
                model=config.model_translator,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Problems with GPT!")
            raise e
