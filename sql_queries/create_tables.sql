-- создание таблицы employees
CREATE TABLE IF NOT EXISTS employees (
                employee_id INT PRIMARY KEY,
                company_name VARCHAR(100) NOT NULL,
                link TEXT,
                description TEXT,
                site_company TEXT,
                count_vacancies INT NOT NULL
                );

-- создание таблицы vacancies
CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id INT PRIMARY KEY,
                employee_id INT REFERENCES employees(employee_id),
                vacancy_name VARCHAR NOT NULL,
                url TEXT,
                salary_from INT,
                salary_to INT,
                city VARCHAR(100)
            );

-- добавление записи в таблицу employees
INSERT INTO employees (employee_id, company_name, link, description, site_company, count_vacancies)
VALUES (%s, %s, %s, %s, %s, %s);

-- добавление записи в таблицу vacancies
INSERT INTO vacancies (vacancy_id, employee_id, vacancy_name, url, salary_from, salary_to, city)
VALUES (%s, %s, %s, %s, %s, %s, %s);
