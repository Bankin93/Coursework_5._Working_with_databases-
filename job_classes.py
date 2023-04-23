import time
from engine_classes import HH
from utils import get_description, get_site, get_employee_data, get_vacancy_city, get_vacancy_name,\
                  get_dump_json, get_vacancy_salary, get_vacancy_id, get_url_vacancy


class HHVacancy:
    """HeadHunter вакансии"""
    hh_vacancies: list = []

    __slots__ = ['employee_id', 'company_name', 'link', 'site_company',
                 'description', 'count_vacancies', 'vacancy_name', 'salary', 'city', 'url_vacancy', 'vacancy_id']

    def __init__(self):
        self.employee_id = None
        self.company_name = None
        self.link = None
        self.site_company = None
        self.description = None
        self.count_vacancies = None
        self.vacancy_name = None
        self.url_vacancy = None
        self.city = None
        self.salary = None
        self.vacancy_id = None

    def get_vacancies_hh(self, text: str):
        """Сбор вакансий из сайта НН и записываем в json"""
        hh = HH(text)
        data = hh.get_request()
        seen_ids = set()
        for item in data.get('items'):
            emp_id = item.get('employer').get('id')
            if emp_id in seen_ids:
                continue
            seen_ids.add(emp_id)
            self.employee_id = emp_id
            self.company_name = item.get('employer').get('name')
            self.link = item.get('employer').get('alternate_url')
            self.site_company = get_site(item)
            self.description = get_description(item)
            self.count_vacancies = get_employee_data(item).get('open_vacancies')
            self.vacancy_id = get_vacancy_id(item)
            self.vacancy_name = get_vacancy_name(item)
            self.url_vacancy = get_url_vacancy(item)
            self.city = get_vacancy_city(item)
            self.salary = []
            try:
                emp_salaries = get_vacancy_salary(item)
                for salary in emp_salaries:
                    currency = salary['currency'] if salary['currency'] is not None else None
                    from_salary = salary['from'] if salary['from'] is not None else 0
                    to_salary = salary['to'] if salary['to'] is not None else 0

                    if currency == 'USD':
                        salary = {'from': round(from_salary * 76.96),
                                  'to': round(to_salary * 76.96)}
                    elif currency == 'EUR':
                        salary = {'from': round(from_salary * 81.11),
                                  'to': round(to_salary * 81.11)}
                    else:
                        salary = {'from': from_salary, 'to': to_salary}
                    self.salary.append(salary)

                HHVacancy.hh_vacancies.append({'employee_id': self.employee_id, 'company_name': self.company_name,
                                               'link': self.link, 'description': self.description,
                                               'site_company': self.site_company,
                                               'count_vacancies': self.count_vacancies, 'vacancy_id': self.vacancy_id,
                                               'vacancy_name': self.vacancy_name, 'url_vacancy': self.url_vacancy,
                                               'city': self.city, 'salary': self.salary})
                time.sleep(0.2)
                if len(HHVacancy.hh_vacancies) >= 10:
                    break
            except (AttributeError, TypeError):
                self.salary = [{'from': 0, 'to': 0}]

        return get_dump_json(HHVacancy.hh_vacancies)
