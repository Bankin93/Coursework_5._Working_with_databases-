import psycopg2
from typing import Any


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о работодателей и вакансий."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                employee_id INT PRIMARY KEY,
                company_name VARCHAR(100) NOT NULL,
                link TEXT,
                description TEXT,
                site_company TEXT,
                count_vacancies INT NOT NULL
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id INT PRIMARY KEY,
                employee_id INT REFERENCES employees(employee_id),
                vacancy_name VARCHAR NOT NULL,
                url TEXT,
                salary_from INT,
                salary_to INT,
                city VARCHAR(100)
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных о работодателях и вакансий в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employee in data:
            cur.execute(
                """
                INSERT INTO employees (employee_id, company_name, link, description, site_company, count_vacancies)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (employee['employee_id'], employee['company_name'], employee['link'], employee['description'],
                 employee['site_company'], employee['count_vacancies'])
            )

            for vacancy_id, vacancy_name, url, city, salary in zip(employee['vacancy_id'], employee['vacancy_name'],
                                                                   employee['url_vacancy'], employee['city'],
                                                                   employee['salary']):

                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, employee_id, vacancy_name, url, salary_from, salary_to, city)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (vacancy_id, employee['employee_id'], vacancy_name, url, salary['from'], salary['to'], city)
                )

    conn.commit()
    conn.close()
