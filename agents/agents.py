from openai import OpenAI


class Agent:
    """
    TODO
    Тут будет класс агента. У каждого агента будет свое назначение, промпт, формат вывода.
    сессию можно будет либо продолжать, либо начинать новую.
    """
    def __init__(self, config, api_key):
        self.api_key = api_key
        self.model = config.model
        self.initial_prompt = config.initial_prompt
        self.output_format = config.output_format if config.output_format is not None else None
        self.session = None

    def _make_new_session(self):
        self.session = OpenAI(api_key=self.api_key)

    def ask(self, message, continue_session=False):
        if not continue_session or self.session is None:
            self._make_new_session()

        pass
