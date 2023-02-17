import requests
import os
from terminaltables import AsciiTable
from dotenv import load_dotenv


def get_vacansies_statistics_hh(language):
    salaries = []
    url = 'https://api.hh.ru/vacancies'
    page = 1
    pages = 2
    area_id = 1
    while page < pages:
        payload = {'text': language, 'area': area_id, 'page': page}

        response = requests.get(url, params=payload)
        response.raise_for_status()
        pages = response.json()['pages']
        vacansies = response.json()['items']
        vacansies_found = response.json()['found']
        for vacancy in vacansies:
            salary = vacancy['salary']
            if salary:
                predicted_salary = predict_rub_salary(salary['from'], salary['to'], salary['currency'])
                if predicted_salary:
                    salaries.append(predicted_salary)
        print(f'скачиваю страницу {page}')
        page += 1
    vacansies_processed = len(salaries)
    if vacansies_processed:
        average_salary = sum(salaries) / vacansies_processed
        average_salary_statistics = {'vacansies_found': vacansies_found, 'vacansies_processed': vacansies_processed, 'average_salary': int(average_salary)}
    return average_salary_statistics


def predict_rub_salary(salary_from, salary_to, salary_currency):
    if salary_currency != 'RUR' and salary_currency != 'rub':
        return
    if salary_from and salary_to:
        return (salary_from + salary_to) // 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8


def get_vacansies_statistics_sj(secret_key, language):
    vacansies_found = 0
    salaries = []
    headers = {'X-Api-App-Id': f'{secret_key}'}
    page = 0
    town = 4
    pages = 1
    while True:
        payload = {'keyword': language, 'town': town, 'page': page}
        url = '	https://api.superjob.ru/2.0/vacancies/'
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        more = response.json()['more']
        print(more)
        print(page)
        if more:
            page += 1
        else:
            break
        vacansies_found = response.json()['total']
        for vacancy in response.json()['objects']:
            salary_currency = vacancy['currency']
            salary_to = vacancy['payment_to']
            salary_from = vacancy['payment_from']
            predicted_salary = predict_rub_salary(salary_from, salary_to, salary_currency)
            if predicted_salary:
                salaries.append(predicted_salary)
    vacansies_processed = len(salaries)
    if vacansies_processed:
        average_salary = sum(salaries) / vacansies_processed
    else:
        average_salary = 0
    average_salary_statistics = {'vacansies_found': vacansies_found, 'vacansies_processed': vacansies_processed,'average_salary': int(average_salary)}
    return average_salary_statistics

def make_table(languages_params, title):
    table_payload = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for language, params in languages_params.items():
        table_payload.append([language, params['vacansies_found'], params['vacansies_processed'], params['average_salary']])
        #
        table_instance = AsciiTable(table_payload, title)
        table_instance.justify_columns[2] = 'right'
    return table_instance.table


if __name__ == "__main__":
    load_dotenv()
    secret_key = os.getenv('SECRET_KEY')
    languages = ['Python', 'Java', 'C++', 'PHP']
    hh_language_params = {}
    sj_language_params = {}
    for language in languages:
        hh_language_params[language] = get_vacansies_hh(language)
        sj_language_params[language] = get_vacansies_sj(secret_key, language)
    print(make_table(hh_language_params, 'Superjob Moscow'))
    print(make_table(sj_language_params, 'HeadHunter Moscow'))