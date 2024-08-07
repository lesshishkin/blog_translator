url_translate_prompt = """
You are a translator. Translate the following URL slug to {language}, and return the
translation in Latin characters (transliteration), keeping hyphens between words:
"""

content_translate_prompt = """
You are a translator. Translate the following text to {language} while preserving any 
HTML tags and other markup exactly as they are in the original text. Do not output anything except the translated text.
The translation must be of excellent quality, preserving the original meaning, and the sentences should be well-formed 
and natural in the specified language. Be attentive to word endings.
IMPORTANT! You must ignore and not translate tags and expressions in curly 
brackets (for example {{link1}}, {{link2}}, {{link3}}), they must remain unchanged!
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

json_diff_prompt = """
You are an assistant tasked with evaluating the quality of translations. You will receive two texts: `original_text` 
and `translated_text`, along with a variable `lang` indicating the language of the translation. Your job is to analyze 
each sentence from the original text and its corresponding sentence in the translated text. You need to determine the 
following for each pair of sentences:

1. Is the translation accurate?
2. Does the meaning remain intact after translation?
3. Is the translated sentence well-phrased?
4. Are there any grammatical or linguistic errors in the translation?
5. Any other relevant characteristics that can help assess the translation quality.

At the end of the analysis, provide an overall rating for the translation from 1 to 5, where:
1. Extremely poor translation
2. Poor translation
3. Mediocre translation
4. Good translation
5. Excellent translation
If there is at least one mistake, inaccuracy or other imperfection of the translation, do not give the highest score

Format your output as follows:

```json
{\
  \"evaluations\": [\
    {\
      \"sentence_number\": 1,\
      \"original_sentence\": \"The quick brown fox jumps over the lazy dog.\",\
      \"translated_sentence\": \"Der schnelle braune Fuchs springt über den faulen Hund.\",\
      \"additional_comments\": \"The translation is precise and natural-sounding.\"\
      \"accuracy\": \"Accurate\",\
      \"meaning_intact\": \"Yes\",\
      \"well_phrased\": \"Yes\",\
      \"errors\": \"None\",\
    },\
    {\
      \"sentence_number\": 2,\
      \"original_sentence\": \"She sells seashells by the seashore.\",\
      \"translated_sentence\": \"Sie verkauft Muscheln am Strand.\",\
      \"additional_comments\": \"The translation fails to capture the playful nature of the original sentence.\"\
      \"accuracy\": \"Inaccurate\",\
      \"meaning_intact\": \"No\",\
      \"well_phrased\": \"Yes\",\
      \"errors\": \"The translation omits the alliteration and specificity of 'seashells by the seashore.'\",\
    }\
  ],\
  \"explanation\": \"While most sentences are accurately translated and well-phrased, some nuances and stylistic elements are occasionally lost.\"\
  \"overall_translation_quality\": 4,\
}
```

Use this format to evaluate the translation quality comprehensively and provide a clear and concise rating and explanation. Do not output anything else.

Original Text:
```
{original_text}
```

Translated Text:
```
{translated_text}
```

Language
```
{language}
```
"""

text_diff_prompt = """
You are an assistant tasked with evaluating the quality of translations. You will receive two texts: `original_text` and `translated_text`, along with a variable `lang` indicating the language of the translation. Your job is to analyze each sentence from the original text and its corresponding sentence in the translated text. You need to determine the following for each pair of sentences:

1. Is the translation accurate?
2. Does the meaning remain intact after translation?
3. Is the translated sentence well-phrased?
4. Are there any grammatical or linguistic errors in the translation?
5. Any other relevant characteristics that can help assess the translation quality.

At the end of the analysis, provide an overall rating for the translation from 1 to 5, where:
1. Extremely poor translation
2. Poor translation
3. Mediocre translation
4. Good translation
5. Excellent translation

Format your output as follows:

```
**Evaluation of Sentence {sentence_number}:**
- Original: {original_sentence}
- Translation: {translated_sentence}
- Accuracy: {accurate/inaccurate}
- Meaning Intact: {yes/no}
- Well-phrased: {yes/no}
- Errors: {list of errors or "None"}
- Additional Comments: {any other observations}

**Overall Translation Quality: {1-5}**
- Explanation: {detailed explanation justifying the rating}
```

Use this format to evaluate the translation quality comprehensively and provide a clear and concise rating and explanation. Do not output anything else.

Original Text:
```
{original_text}
```

Translated Text:
```
{translated_text}
```

Language
```
{language}
```
"""
