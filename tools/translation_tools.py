from tools.gpt_tools import ask_gpt
from configs.configs import config
import evaluate
from configs.prompts import url_translate_prompt, content_translate_prompt, content_diff_prompt, basic_translate_prompt


def translate_post(post_data, language, debug=False):
    prompt = basic_translate_prompt.format(language=config.langs[language])
    text = post_data['title']
    translated_title = ask_gpt(prompt, text)
    if debug:
        print('Title translated')

    if post_data['excerpt'] is not None:
        prompt = basic_translate_prompt.format(language=config.langs[language])
        text = post_data['excerpt']
        translated_excerpt = ask_gpt(prompt, text)
    else:
        translated_excerpt = ""
    if debug:
        print('Excerpt translated')

    prompt = content_translate_prompt.format(language=config.langs[language])
    text = post_data['content']
    translated_content = ask_gpt(prompt, text)
    if debug:
        print('Content translated')

    prompt = url_translate_prompt.format(language=config.langs[language])
    text = post_data['link'].split('/')[-1]
    translated_slug = ask_gpt(prompt, text)

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
    bleu_score = metric.compute(double_translated_text, [original_text])

    # попросим модель сравнить два текста, дать оценку и процитировать неудачные места перевода
    prompt = content_diff_prompt.format(original_text=original_text, double_translated_text=double_translated_text)
    gpt_score = ask_gpt(prompt)

    return bleu_score['bleu'], gpt_score


def clean_text(text: str):
    filter_list = ["<!-- wp:paragraph -->", "<!-- /wp:paragraph -->", "<p>", "</p>"]
    for item in filter_list:
        text = text.replace(item, "")
    return text


def localize_links(post_data, language):
    # эта функция будет сканировать статью на предмет ссылок. искать совпадения в базе, подставлять в текст
    # переведенные ссылки
    pass
