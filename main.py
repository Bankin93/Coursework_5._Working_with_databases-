import pandas as pd
from job_classes import HHVacancy
from utils import get_load_json
from config import config
from postgres_db import create_database, save_data_to_database
from dbmanager import DBManager


def main():
    params = config()

    # Задаем параметры для вывода таблицы
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 200)
    pd.set_option('display.max_rows', 100)

    input_word = input('Введите ключевое слово вакансии для сбора данных:\n')
    print('================================================================')
    print('Идет загрузка данных...')

    vacancy = HHVacancy()
    vacancy.get_vacancies_hh(input_word)

    print('Идет формирование базы данных...')
    load_data = get_load_json()
    create_database('head_hunter', params)
    save_data_to_database(load_data, 'head_hunter', params)
    print('Данные загружены. Готовы для работы!')
    print('================================================================')

    db = DBManager('head_hunter', params)
    while True:
        print('Меню:\n'
              '1 - вывести таблицу всех компаний и количество вакансий у каждой компании\n'
              '2 - вывести таблицу всех вакансий\n'
              '3 - вывести таблицу среднюю зарплату по вакансиям\n'
              '4 - вывести таблицу всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
              '5 - вывести таблицу всех вакансий, в названии которых содержатся ваше переданное слово\n'
              'stop - закончить работу')
        print('================================================================')
        user_input = input("Введите вариант из предложенного меню:\n")
        if user_input == '1':
            print(db.get_companies_and_vacancies_count())

        elif user_input == '2':
            print(db.get_all_vacancies())

        elif user_input == '3':
            print(db.get_avg_salary())

        elif user_input == '4':
            print(db.get_vacancies_with_higher_salary())

        elif user_input == '5':
            print(db.get_vacancies_with_keyword(input_word))

        elif user_input.lower() == 'stop':
            print('Программа завершена!')
            break

        else:
            print("Такого из предложенных вариантов нет!\nПопробуйте еще раз!")
            print('================================================================')
            continue

        print('================================================================')
        print('Показать еще меню? Yes/No')
        choice = input().lower()
        print('================================================================')
        while choice not in ['yes', 'no']:
            print('Неверный ввод!\nПопробуйте еще раз!')
            choice = input().lower()
            print('================================================================')
        if choice == 'no':
            print('Программа завершена!')
            break


if __name__ == '__main__':
    main()
