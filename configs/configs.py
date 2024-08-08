from easydict import EasyDict
from configs.prompts import content_translate_prompt, evaluation_prompt, editor_prompt
from configs.structures import TranslationEvaluation

config = EasyDict()

config.blog_url = "https://get.it.com/blog/"

# config.langs = {'ru': 'Russian',
#                 'es': 'Spanish'}
config.langs = {'ru': 'Russian'}
config.origin_lang = "English"
config.model = "gpt-4o-2024-08-06"

# Список кодов языков для transliterate
config.transliterate_languages = ['ru', 'uk', 'be', 'bg', 'mk', 'sr', 'hy', 'el']
# Список кодов языков для unidecode
config.unidecode_languages = ['es', 'en', 'fr', 'de', 'it', 'pt', 'nl', 'sv', 'da', 'fi', 'no']

# То, что удаляем перед подсчетом BLEU
# TODO расширить список для большей точности метрики
config.filter_list = ["<!-- wp:paragraph -->", "<!-- /wp:paragraph -->", "<p>", "</p>"]


# классы агентов пока не используются, это на вырост
# Translator Agent Configuration
config.translation_agent = EasyDict()
config.translation_agent.model = "gpt-4o"
config.translation_agent.system_prompt = content_translate_prompt
config.translation_agent.output_format = None

# Editor Agent Configuration
config.editor_agent = EasyDict()
config.editor_agent.model = "gpt-4o"
config.editor_agent.system_prompt = editor_prompt
config.editor_agent.output_format = None

# Evaluator Agent Configruration
config.evaluator_agent = EasyDict()
config.evaluator_agent.model = "gpt-4o-2024-08-06-4o"       # JSON-ready model
config.evaluator_agent.system_prompt = evaluation_prompt
config.evaluator_agent.output_format = TranslationEvaluation
