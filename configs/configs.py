from easydict import EasyDict

config = EasyDict()

config.blog_url = "https://get.it.com/blog/"

config.langs = {'ru': 'Russian',
                'es': 'Spanish'}
# config.langs = {'ru': 'Russian'}
config.origin_lang = "English"
config.model = "gpt-4o-2024-08-06"

# Список кодов языков для transliterate
config.transliterate_languages = ['ru', 'uk', 'be', 'bg', 'mk', 'sr', 'hy', 'el']
# Список кодов языков для unidecode
config.unidecode_languages = ['es', 'en', 'fr', 'de', 'it', 'pt', 'nl', 'sv', 'da', 'fi', 'no']

# То, что удаляем перед подсчетом BLEU
# TODO расширить список для большей точности метрики
config.filter_list = ["<!-- wp:paragraph -->", "<!-- /wp:paragraph -->", "<p>", "</p>"]