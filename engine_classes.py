from abc import ABC, abstractmethod
import requests


class Engine(ABC):
    """Абстрактный класс Engine для сбора информации через API"""
    @abstractmethod
    def get_request(self, url: str, params: dict, headers: dict):
        """Запрос через API"""
        resp = requests.get(url=url, params=params, headers=headers)
        return resp.json()


class HH(Engine):
    """Класс НН наследуемый от класса Engine"""
    def __init__(self, text: str):
        self.text = text
        self.params = {'text': self.text, 'per_page': 100, 'page': 0, 'area': 113}
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    def get_request(self, **kwargs):
        return super().get_request(self.url, self.params, self.headers)
