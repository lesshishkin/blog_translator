from tools.gpt_tools import ask_gpt
from configs.configs import config
import evaluate
from configs.prompts import url_translate_prompt, content_translate_prompt, content_diff_prompt, basic_translate_prompt
from transliterate import translit
import re
from unidecode import unidecode


def translate_post(post_data, language, debug=False):
    if 'title' not in post_data or 'content' not in post_data:
        raise KeyError('post_data должен содержать ключи "title" и "content"')

    # title
    prompt = basic_translate_prompt.format(language=config.langs[language])
    text = post_data['title']
    translated_title = ask_gpt(prompt, text)
    if debug:
        print('Title translated')

    # excerpt
    if len(post_data['excerpt']) != 0:
        prompt = basic_translate_prompt.format(language=config.langs[language])
        text = post_data['excerpt']
        translated_excerpt = ask_gpt(prompt, text)
    else:
        translated_excerpt = ""
    if debug:
        print('Excerpt translated')

    # content
    prompt = content_translate_prompt.format(language=config.langs[language])
    text = post_data['content']
    translated_content = ask_gpt(prompt, text)
    if debug:
        print('Content translated')

    # link and slug
    translated_slug = urlify(translated_title, language)
    translated_url = config.blog_url + translated_slug
    if debug:
        print('Slug translated')

    return translated_title, translated_excerpt, translated_content, translated_slug, translated_url


def evaluate_translation(translation, original_text):
    # translate the translation back to original lang
    prompt = content_translate_prompt.format(language=config.origin_lang)
    double_translated_text = clean_text(ask_gpt(prompt, translation))
    original_text = clean_text(original_text)

    # calculate BLEU score
    metric = evaluate.load("bleu")
    bleu_score = metric.compute(predictions=[double_translated_text], references=[[original_text]])

    # попросим модель сравнить два текста, дать оценку и процитировать неудачные места перевода
    prompt = content_diff_prompt.format(original_text=original_text, double_translated_text=double_translated_text)
    gpt_score = ask_gpt(prompt)

    return bleu_score['bleu'], gpt_score


def clean_text(text: str):
    for item in config.filter_list:
        text = text.replace(item, "")
    return text


def localize_links(post_data, language):
    # эта функция будет сканировать статью на предмет ссылок. искать совпадения в базе, подставлять в текст
    # переведенные ссылки
    pass


def urlify(text, lang):
    # если текст кирилический, то transliterate, если алфавит латинский, то unidecode
    if lang in config.transliterate_languages:
        transliterated_text = translit(value=text, language_code=lang, reversed=True)
    elif lang in config.unidecode_languages:
        transliterated_text = unidecode(text)
    else:
        raise Exception('Unknown language!')

    transliterated_text = re.sub(r'\s+', '-', transliterated_text)
    urlified_text = re.sub(r'[^a-zA-Z0-9\-]', '', transliterated_text)
    urlified_text = urlified_text.lower()

    return urlified_text
