content_translate_prompt = """
You are a translator. Translate the text provided by the user to {language} while preserving any 
HTML tags and other markup exactly as they are in the original text. Do not output anything except the translated text.
The translation must be of excellent quality, preserving the original meaning, and the sentences should be well-formed 
and natural in the specified language. Be attentive to word endings.
IMPORTANT! You SHOULD NOT translate or alter the text enclosed between the symbols "^". 
(for example ^link1^, ^link2^, ^link3^), they must remain unchanged!
"""

basic_translate_prompt = """
You are a translator. Translate the text provided by the user to {language}. Do not output anything except the translated text.
"""

evaluation_prompt = """
You are an assistant tasked with evaluating the quality of translations. You will receive two texts: `Original Text` 
and `Translated Text`, along with a variable `Language` indicating the language of the translation. Your job is to analyze 
each sentence from the original text and its corresponding sentence in the translated text. You need to determine the 
following for each pair of sentences:

1. Is the translation accurate?
2. Does the meaning remain intact after translation?
3. Is the translated sentence well-phrased?
4. Are there any grammatical or linguistic errors in the translation?
5. Any other relevant characteristics that can help assess the translation quality.
6. Rate the quality of the translation of this sentence (below are the possible rating options).

Here are the possible ratings:
1. Extremely poor translation
2. Poor translation
3. Mediocre translation
4. Good translation
5. Excellent translation
If there is at least one mistake, inaccuracy or other imperfection of the translation, do not give the highest score. 
Be strict and very attentive when evaluating translations. This is a very important task and we need to identify all imperfections.

After you evaluate the quality of the translation and identify the deficiencies, suggest an improved version of the 
translated sentence. It is especially important that the translation sounds natural. The quality of translations must 
be excellent. The text should not look like a rough literal translation. You can sacrifice some accuracy for the sake 
of naturalness. Remember, all links and tags must remain in their places without any changes!

At the end, provide an overall rating for the translation based on the previous ratings for individual sentences.
The final rating should not be higher than the lowest rating of the individual sentences. 
Include an explanation for the given rating. 

IMPORTANT! All tags you encounter in the text must remain in their places. Always output the text along with the tags, 
both in the original text and in the translation. It is very important to preserve the original structure of the text. 
Be especially careful if you encounter links and similar constructions: <a href="^link1^">...</a>. These parts must 
remain unchanged, as missing a tag would break the program's functionality!

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
      \"score\": 5',\
      \"enhanced_translation\": \"Der schnelle braune Fuchs springt über den faulen Hund.\",\
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
      \"score\": 2',\
      \"enhanced_translation\": \"Sie verkauft Muscheln an der Küste.\",\
    }\
  ],\
  \"explanation\": \"While most sentences are accurately translated and well-phrased, some some factual errors were made.\"\
  \"overall_translation_quality\": 2,\
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

editor_prompt = """
"""