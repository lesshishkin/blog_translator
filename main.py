from create_wxr import create_wxr
from parse_xml import parse_xml
from dotenv import load_dotenv
import os
# from pprint import pprint
from configs import config
from openai import OpenAI
# import transliterate
import evaluate

load_dotenv('.env')
API_KEY = os.environ['GPT_API_KEY']


def translate_post(post_data, language):
    prompt = f"You are a translator. Translate the following text to {config.langs[language]}."
    text = post_data['title']
    translated_title = ask_gpt(prompt, text)
    print('Title translated')

    if post_data['excerpt'] is not None:
        prompt = f"You are a translator. Translate the following text to {config.langs[language]}."
        text = post_data['excerpt']
        translated_excerpt = ask_gpt(prompt, text)
    else:
        translated_excerpt = ""
    print('Excerpt translated')

    prompt = (f"You are a translator. Translate the following text to {config.langs[language]} while preserving any "
              f"HTML tags and other markup exactly as they are in the original text:")
    text = post_data['content']
    translated_content = ask_gpt(prompt, text)
    print('Content translated')

    prompt = (f"You are a translator. Translate the following URL slug to {config.langs[language]}, and return the "
              f"translation in Latin characters (transliteration), keeping hyphens between words:")
    text = post_data['link'].split('/')[-1]
    translated_slug = ask_gpt(prompt, text)

    translated_url = config.blog_url + translated_slug
    print('Slug translated')

    return translated_title, translated_excerpt, translated_content, translated_slug, translated_url


def evaluate_translation(translation, original_text):
    # translate the translation back to original lang
    prompt = (f"You are a translator. Translate the following text to {config.origin_lang} while preserving any "
              f"HTML tags and other markup exactly as they are in the original text:")
    double_translated_text = ask_gpt(prompt, translation)
    # calculate BLEU score
    metric = evaluate.load("bleu")
    bleu_score = metric.compute(double_translated_text, [original_text])
    # попросим модель сравнить два текст
    prompt = f"""
    You are a translation evaluator. Compare the original text and the back-translated text, ignoring any HTML tags and markup. Provide a score from 1 to 5 where:
    1 - Extremely poor translation
    2 - Poor translation
    3 - Mediocre translation
    4 - Good translation
    5 - Excellent translation

    Additionally, quote the places in the back-translated text and the original text where the meaning has changed or been lost during the translation process, ignoring any HTML tags and markup.

    Original Text:
    {original_text}

    Back-translated Text:
    {double_translated_text}
    """
    gpt_score = ask_gpt(prompt)

    return bleu_score['bleu'],gpt_score


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

    return translation['choices'][0]['message']['content']


def localize_links(post_data, language):
    pass


if __name__ == '__main__':
    post_path = 'getitcom.WordPress.2024-08-01.xml'
    original_post_data = parse_xml(post_path)

    translations = []

    for lang in config.langs.keys():
        title, excerpt, content, slug, link = translate_post(original_post_data, lang)
        bleu_score, gpt_score = evaluate_translation(content, original_post_data['content'])
        print('Language:  ', lang)
        print('BLEU score:', bleu_score)
        print(gpt_score)

        # todo links localization
        # translated_data = localize_links(content, lang)

        # todo разобраться со всеми полями
        post = {
            'title': title,
            'link': link,
            'pubDate': original_post_data['pubDate'],
            'creator': original_post_data['creator'],
            # 'guid': guid,
            'content': content,
            'excerpt': excerpt,
            # 'post_id': post_id,
            'post_date': original_post_data['post_date'], #CDATA
            'post_date_gmt': original_post_data['post_date_gmt'], #CDATA
            'post_name': slug,  #CDATA
            # 'status': status,
            # 'post_parent': post_parent,
            # 'menu_order': menu_order,
            'post_type': original_post_data['post_type'],   #CDATA
            # 'is_sticky': is_sticky,
            # 'category': category_nicename,
        }

        translations.append(post)

    #   тест перевода:
    #       переводим
    #       переводи назад
    #       считаем BLEU
    #       подаем в гпт с промптом сравнить и выявить несоответствия

    output_path = 'output_' + post_path
    create_wxr(translations, output_path)
