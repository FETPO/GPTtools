import requests


class Prompt:
    """Prompt class"""

    def __init__(self, template, **kwargs):
        self.template: str = template
        self.kwargs: dict = kwargs

    def __str__(self) -> str:
        return self.template

    def construct(self):
        """Construct the prompt"""
        # Look for the keys in the template from the kwargs
        for key in self.kwargs.items():
            # If the key is in the template, replace it with the value
            if key[0] in self.template:
                self.template = self.template.replace(key[0], key[1])
        return self.template


class OpenAI:
    """OpenAI API wrapper"""

    def __init__(self, api_key, config=None):
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        if config:
            self.config = config
        else:
            self.config = {
                "model": "text-davinci-003",
                "prompt": "Say this is a test",
                "max_tokens": 7,
                "temperature": 0,
                "top_p": 1,
                "n": 1,
                "stream": False,
                "logprobs": None,
                "stop": "\n"
            }

    def query(self, prompt: str, model: str = None, max_tokens: int = None, temperature: float = None, top_p: float = None, n: int = None, stream: bool = None, logprobs: int = None, stop: str or list = None, **kwargs) -> dict:
        """Query the OpenAI API"""

        completions_endpoint = "https://api.openai.com/v1/completions"
        config = {
            "model": model or self.config["model"],
            "prompt": prompt,
            "max_tokens": max_tokens or self.config["max_tokens"],
            "temperature": temperature or self.config["temperature"],
            "top_p": top_p or self.config["top_p"],
            "n": n or self.config["n"],
            "stream": stream or self.config["stream"],
            "logprobs": logprobs or self.config["logprobs"],
            "stop": stop or self.config["stop"]
        }
        config.update(kwargs)
        response = requests.post(completions_endpoint,
                                 headers=self.headers, json=config, timeout=60)
        return response.json()
