import psycopg2
import pandas as pd
from config import config
from typing import Any


class DBManager:
    """Класс DBManager содержит методы для работы с БД"""
    def __init__(self, database_name: str, params: dict):
        self.dbname = database_name
        self.params = config()
        self.conn = psycopg2.connect(dbname=database_name, **params)

    def execute_query(self, query: str, fetch=False) -> list[tuple[Any]]:
        with self.conn.cursor() as cur:
            cur.execute(query)
            if fetch:
                return cur.fetchall()

    def get_companies_and_vacancies_count(self) -> pd.DataFrame:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        query = """
                SELECT company_name, count_vacancies
                FROM employees 
                ORDER BY count_vacancies DESC;
                """
        rows = self.execute_query(query, fetch=True)
        df = pd.DataFrame(rows, columns=['company_name', 'count_vacancies'], index=range(1, len(rows) + 1))
        return df

    def get_all_vacancies(self) -> pd.DataFrame:
        """Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию."""
        query = """         
                SELECT e.company_name, v.vacancy_name, v.city, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employees e USING (employee_id)
                ORDER BY company_name;
                """
        rows = self.execute_query(query, fetch=True)
        df = pd.DataFrame(rows, columns=['company_name', 'vacancy_name', 'city', 'salary_From', 'salary_to', 'url'],
                          index=range(1, len(rows) + 1))
        return df

    def get_avg_salary(self) -> pd.DataFrame:
        """Получает среднюю зарплату по вакансиям."""
        query = """         
                SELECT ROUND(AVG(salary_to + salary_from) / 2) as avg_salary
                FROM vacancies;
                """
        rows = self.execute_query(query, fetch=True)
        df = pd.DataFrame(rows, columns=['average_salary'], index=range(1, 1+1))
        return df

    def get_vacancies_with_higher_salary(self) -> pd.DataFrame:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        query = """
                SELECT company_name, v.* FROM employees
                JOIN vacancies v USING (employee_id)
                WHERE (salary_from + salary_to) / 2 > (SELECT ROUND(AVG(salary_to + salary_from) / 2) FROM vacancies)
                ORDER BY (v.salary_from + v.salary_to) / 2 DESC;
                """
        rows = self.execute_query(query, fetch=True)
        df = pd.DataFrame(rows, columns=['company_name', 'vacancy_id', 'employee_id', 'vacancy_name', 'url',
                                         'Salary From', 'Salary To', 'city'], index=range(1, len(rows) + 1))
        return df

    def get_vacancies_with_keyword(self, keyword: str) -> pd.DataFrame:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        query = f"""
                SELECT company_name, v.* FROM employees
                JOIN vacancies v USING (employee_id)
                WHERE LOWER(vacancy_name) 
                LIKE LOWER('%{keyword}%') 
                ORDER BY company_name;
                """
        rows = self.execute_query(query, fetch=True)
        df = pd.DataFrame(rows,
                          columns=['company_name', 'vacancy_id', 'employee_id', 'vacancy_name', 'url', 'Salary From',
                                   'Salary To', 'city'], index=range(1, len(rows) + 1))
        return df
