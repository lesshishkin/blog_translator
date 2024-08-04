from create_wxr import create_wxr
from parse_xml import parse_xml
from configs import config
from translation_tools import evaluate_translation, translate_post
# from pprint import pprint
# import transliterate

if __name__ == '__main__':
    post_path = 'input/getitcom.WordPress.2024-08-01.xml'
    original_post_data = parse_xml(post_path)

    translations = []

    for lang in config.langs.keys():
        title, excerpt, content, slug, link = translate_post(original_post_data, lang, debug=True)
        bleu_score, gpt_score = evaluate_translation(content, original_post_data['content'])
        print('Language:  ', lang)
        print('BLEU score:', bleu_score)
        print('GPT score: ', gpt_score)

        # todo links localization
        # проблема переведнных ссылок в том, что ты не можешь быть уверен что статья получила аппрув и запощена.
        # как вариант можно просто чекать доступность ссылки перед подстановкой, но это как-то примитивно.
        # было бы здорово иметь внешний источник правды отностительно ссылок

        # translated_data = localize_links(content, lang)

        # todo разобраться со всеми полями, какие именно нужны
        # todo раобраться где CDATA, где не CDATA
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

    output_path = 'output_' + post_path
    create_wxr(translations, output_path)
    print('File created:', output_path)
