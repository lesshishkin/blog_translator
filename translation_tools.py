from gpt_tools import ask_gpt
from configs import config
import evaluate


def translate_post(post_data, language, debug=False):
    prompt = f"You are a translator. Translate the following text to {config.langs[language]}."
    text = post_data['title']
    translated_title = ask_gpt(prompt, text)
    if debug:
        print('Title translated')

    if post_data['excerpt'] is not None:
        prompt = f"You are a translator. Translate the following text to {config.langs[language]}."
        text = post_data['excerpt']
        translated_excerpt = ask_gpt(prompt, text)
    else:
        translated_excerpt = ""
    if debug:
        print('Excerpt translated')

    prompt = (f"You are a translator. Translate the following text to {config.langs[language]} while preserving any "
              f"HTML tags and other markup exactly as they are in the original text:")
    text = post_data['content']
    translated_content = ask_gpt(prompt, text)
    if debug:
        print('Content translated')

    prompt = (f"You are a translator. Translate the following URL slug to {config.langs[language]}, and return the "
              f"translation in Latin characters (transliteration), keeping hyphens between words:")
    text = post_data['link'].split('/')[-1]
    translated_slug = ask_gpt(prompt, text)

    translated_url = config.blog_url + translated_slug
    if debug:
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
    # попросим модель сравнить два текста, дать оценку и процитировать неудачные места перевода
    prompt = f""" You are a translation evaluator. Compare the original text and the back-translated text, 
    ignoring any HTML tags and markup. Provide a score from 1 to 5 where: 1 - Extremely poor translation, 2 - Poor 
    translation, 3 - Mediocre translation, 4 - Good translation, 5 - Excellent translation

    Additionally, quote the places in the back-translated text and the original text where the meaning has changed or 
    been lost during the translation process.

    Original Text:
    {original_text}

    Back-translated Text:
    {double_translated_text}
    """
    gpt_score = ask_gpt(prompt)

    return bleu_score['bleu'], gpt_score


def localize_links(post_data, language):
    # эта функция будет сканировать статью на предмет ссылок. искать совпадения в базе, подставлять в текст
    # переведенные ссылки
    pass
