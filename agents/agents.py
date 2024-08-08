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
        self.system_prompt = config.system_prompt
        self.output_format = config.output_format if config.output_format is not None else None
        self.session = None
        self.messages = []

    def _make_new_session(self):
        self.session = OpenAI(api_key=self.api_key)
        self.messages = []
        self.messages.append({"role": "system", "content": self.system_prompt})

    def ask(self, text, continue_session=False):
        if not continue_session or self.session is None:
            self._make_new_session()

        self.messages.append({"role": "user", "content": text})

        if self.output_format is not None:
            # если надо получить json в ответ
            try:
                response = self.session.beta.chat.completions.parse(
                    model=self.model,
                    messages=self.messages,
                    response_format=self.output_format,
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Problems with GPT!")
                raise e
        else:
            try:
                response = self.session.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Problems with GPT!")
                raise e
