from create_wxr import create_wxr
from parse_xml import parse_xml
from prompts import url_translate_prompt, content_translate_prompt
from dotenv import load_dotenv
import os
from pprint import pprint

langs = ['ru', 'es']


def gpt_translate(post_data, language):
    pass


def localize_links(post_data, language):
    pass


if __name__ == '__main__':
    load_dotenv('.env')
    api_key = os.environ['GPT_API_KEY']

    post_path = 'getitcom.WordPress.2024-08-01.xml'
    original_post_data = parse_xml(post_path)

    translations = []

    # for lang in langs:
    #     translated_data = gpt_translate(original_post_data, lang)
    #     # todo links localization
    #     # translated_data = localize_links(translated_data, lang)
    #     translations.append(translated_data)

    translations.append(original_post_data)
    output_path = 'output_' + post_path
    # pprint(original_post_data)
    create_wxr(translations, output_path)

    # Пример использования
    posts = [
        {
            "title": "First Post",
            "link": "http://yourblog.com/first-post",
            "pubDate": "Fri, 01 Jan 2021 00:00:00 +0000",
            "author": "admin",
            "content": "<p>This is the content of the first post.</p>",
            "excerpt": "This is the excerpt of the first post.",
            "id": 1,
            "post_date": "2021-01-01 00:00:00",
            "post_date_gmt": "2021-01-01 00:00:00",
            "status": "publish",
            "post_type": "post",
        },
        # Добавьте больше постов, если необходимо
    ]

    # create_wxr(posts, 'output.xml')