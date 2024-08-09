from tools.gpt_tools import ask_gpt
from configs.configs import config
import evaluate
from configs.prompts import content_translate_prompt, basic_translate_prompt, evaluation_prompt
from transliterate import translit
import re
from unidecode import unidecode
from configs.structures import TranslationEvaluation
from configs.dictionaries import dicts


def translate_post(post_data, api_key, language, debug=False):
    if 'title' not in post_data or 'content' not in post_data:
        raise KeyError('post_data должен содержать ключи "title" и "content"')

    # title
    prompt = basic_translate_prompt.format(language=config.langs[language])
    if language in dicts:
        prompt = '\n'.join([prompt, dicts[language]])
    text = post_data['title']
    translated_title = ask_gpt(prompt, api_key, text)
    if debug:
        print('Title translated')

    # excerpt
    if len(post_data['excerpt']) != 0:
        prompt = basic_translate_prompt.format(language=config.langs[language])
        if language in dicts:
            prompt = '\n'.join([prompt, dicts[language]])
        text = post_data['excerpt']
        translated_excerpt = ask_gpt(prompt, api_key, text)
    else:
        translated_excerpt = ""
    if debug:
        print('Excerpt translated')

    # content
    # убираем ссылки перед подачей в gpt
    text_without_links, links = replace_links(post_data['content'])
    prompt = content_translate_prompt.format(language=config.langs[language])
    if language in dicts:
        prompt = '\n'.join([prompt, dicts[language]])
    translated_content = ask_gpt(prompt, api_key, text_without_links)
    # возвращаем ссылки
    text_with_links = restore_links(translated_content, links)

    if debug:
        print('Content translated')

    # link and slug
    translated_slug = urlify(translated_title, language)
    translated_url = config.blog_url + translated_slug
    if debug:
        print('Url and Slug translated')

    return translated_title, translated_excerpt, text_with_links, translated_slug, translated_url


def enhance_translation(translation, original_text, language, api_key, compute_bleu=False):
    if compute_bleu:
        # translate the translation back to original lang
        prompt = content_translate_prompt.format(language=config.origin_lang)
        double_translated_text = clean_text(ask_gpt(prompt, api_key, translation))
        cleaned_original_text = clean_text(original_text)

        # calculate BLEU score
        metric = evaluate.load("bleu")
        bleu_score = metric.compute(predictions=[double_translated_text], references=[[cleaned_original_text]])['bleu']
    else:
        bleu_score = None

    # попросим модель сравнить два текста, дать оценку и процитировать неудачные места перевода
    # а также улучшить!
    prompt = (evaluation_prompt.
              replace("{original_text}", original_text).
              replace('{translated_text}', translation).
              replace("{language}", config.langs[language]))
    if language in dicts:
        prompt = '\n'.join([prompt, dicts[language]])
    gpt_score = ask_gpt(prompt, api_key, response_format=TranslationEvaluation)

    return bleu_score, gpt_score


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


def replace_links(text):
    link_pattern = re.compile(r'<a\s+href="([^"]+)">([^<]+)</a>', re.IGNORECASE)

    links_dict = {}
    counter = 1

    def replace_link(match):
        nonlocal counter
        url = match.group(1)
        link_text = match.group(2)
        placeholder = f"^link{counter}^"
        links_dict[placeholder] = url
        counter += 1
        return f'<a href="{placeholder}">{link_text}</a>'

    new_text = link_pattern.sub(replace_link, text)

    return new_text, links_dict


def restore_links(text, links_dict):
    placeholder_pattern = re.compile(r'\^link\d+\^')

    def replace_placeholder(match):
        placeholder = match.group(0)
        url = links_dict.get(placeholder, placeholder)
        return url

    restored_text = placeholder_pattern.sub(replace_placeholder, text)

    return restored_text


def multi_translate_content():
    pass
