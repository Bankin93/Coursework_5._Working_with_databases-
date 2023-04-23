import requests
from bs4 import BeautifulSoup
import json


def get_employee_data(data: dict) -> dict:
    """Возвращает данные о работодателе из HH API в виде словаря"""
    emp_url = data.get('employer').get('url')
    emp_data = requests.get(emp_url).json()
    return emp_data


def get_description(data: dict) -> str | None:
    """Возвращает отформантированное описание компании"""
    emp_data = get_employee_data(data)
    text = emp_data.get('description')
    if text is None:
        return None
    else:
        soup = BeautifulSoup(text, 'html.parser')
        description = soup.get_text()
        return description


def get_site(data: dict) -> str | None:
    """Возвращает URL-адрес сайта работодателя из HH"""
    emp_data = get_employee_data(data)
    site = emp_data.get('site_url')
    if site is None or site == '':
        return None
    else:
        return site


def get_item_vacancy(data: dict) -> dict:
    """Возвращает словарь вакансий компании"""
    emp_data = get_employee_data(data)
    vac_url = emp_data.get('vacancies_url')
    resp = requests.get(vac_url).json()
    vac_data = resp.get('items')
    return vac_data


def get_url_vacancy(data: dict) -> list[str]:
    """Возвращает список ссылок на вакансии компании"""
    url = [vac.get('alternate_url') for vac in get_item_vacancy(data)]
    return url


def get_vacancy_name(data: dict) -> list[str]:
    """Возвращает список названий вакансий компании"""
    vacancy = [vac.get('name') for vac in get_item_vacancy(data)]
    return vacancy


def get_vacancy_id(data: dict) -> list:
    """Возвращает список id вакансий"""
    vac_id = [vac.get('id') for vac in get_item_vacancy(data)]
    return vac_id


def get_vacancy_city(data: dict) -> list[str]:
    """Возвращает список городов вакансий"""
    cities = []
    for city in get_item_vacancy(data):
        cities.append(city.get('area').get('name'))
    return cities


def get_vacancy_salary(data: dict) -> list[dict]:
    """Возвращает список словарей зарплаты вакансий"""
    salaries = []
    for sal in get_item_vacancy(data):
        salaries.append(sal.get('salary'))
    return salaries


def get_dump_json(data: list[dict]) -> json:
    """Записывает собранный список вакансий в json"""
    with open('hh_vacancy.json', 'w', encoding='utf-8') as f:
        return json.dump(data, f, indent=2, ensure_ascii=False)


def get_load_json():
    """Считывает данные из json"""
    with open('hh_vacancy.json', 'r', encoding='utf-8') as f:
        my_loaded_list = json.load(f)
        return my_loaded_list
