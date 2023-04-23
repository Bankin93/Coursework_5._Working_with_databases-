-- просмотр всех записей таблицы employees
SELECT * FROM employees;

-- просмотр всех записей таблицы vacancies
SELECT * FROM vacancies;

-- Получает список всех компаний и количество вакансий у каждой компании
SELECT company_name, count_vacancies
FROM employees
ORDER BY count_vacancies DESC;

-- Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
SELECT e.company_name, v.vacancy_name, v.city, v.salary_from, v.salary_to, v.url
FROM vacancies v
JOIN employees e USING (employee_id)
ORDER BY company_name;

-- Получает среднюю зарплату по вакансиям
SELECT ROUND(AVG(salary_to + salary_from) / 2) as avg_salary
FROM vacancies;

-- Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
SELECT company_name, v.* FROM employees
JOIN vacancies v USING (employee_id)
WHERE (salary_from + salary_to) / 2 > (SELECT ROUND(AVG(salary_to + salary_from) / 2) FROM vacancies)
ORDER BY (v.salary_from + v.salary_to) / 2 DESC;

-- Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”
SELECT company_name, v.* FROM employees
JOIN vacancies v USING (employee_id)
WHERE LOWER(vacancy_name)
LIKE LOWER('%{keyword}%')
ORDER BY company_name;
