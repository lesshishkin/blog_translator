url_translate_prompt = """
You are a translator. Translate the following URL slug to {language}, and return the
translation in Latin characters (transliteration), keeping hyphens between words:
"""

content_translate_prompt = """
You are a translator. Translate the following text to {language} while preserving any 
HTML tags and other markup exactly as they are in the original text. Do not output anything except the translated text.
Text:
"""

content_diff_prompt = """
You are a translation evaluator. Compare the original text and the back-translated text, 
ignoring any HTML tags and markup. Provide a score from 1 to 5 where: 1 - Extremely poor translation, 2 - Poor 
translation, 3 - Mediocre translation, 4 - Good translation, 5 - Excellent translation

Additionally, quote the places in the back-translated text and the original text where the meaning has changed or 
been lost during the translation process.

Original Text:
{original_text}

Back-translated Text:
{double_translated_text}
"""

basic_translate_prompt = """
You are a translator. Translate the following text to {language}. Do not output anything except the translated text.
Text:
"""
