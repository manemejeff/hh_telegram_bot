import requests
import html2text
from random import randint, shuffle

BASE_URL = 'http://api.hh.ru/'
langs = [
    'python', 'java', 'kotlin', 'swift', 'c#', 'c', 'c++',
    'go', 'php', 'java-script', 'vba', 'sql', 'ruby', 'groovy',
    'perl', 'rust', 'delphi', 'shell', '1с', 'rpa'
]
PROFS = [
    "уборщик",
    "дворник",
    "полотёр",
    "теплотрасса",
    "грузчик"
]


def get_vacancies_by_lang(lang):
    response = requests.get(f'https://api.hh.ru/vacancies?text={lang}&area=1586')
    # print(response.json())
    result = parse_vacancy(response.json())
    yield from result


def get_random_vacancy():
    shuffle(PROFS)
    response = requests.get(f'https://api.hh.ru/vacancies?text={PROFS[0]} OR {PROFS[1]}')
    if response.status_code == 200:
        yield from parse_vacancy(response.json())


def parse_json(json_item):
    result = ''
    salary = ''
    if json_item['salary']:
        salary += f"от {json_item['salary']['from']} " if json_item['salary']['from'] else ""
        salary += f"до {json_item['salary']['to']} " if json_item['salary']['to'] else ""
        salary += f"{json_item['salary']['currency']}" if json_item['salary']['currency'] else ""
    else:
        salary = "Не указана"
    addres = json_item['address']['raw'] if json_item['address'] else "Не указан"
    employer = json_item['employer']['name'] if json_item['employer'] else "Не указана"
    if 'description' in json_item.keys():
        description = html2text.html2text(json_item['description'])
    else:
        description = 'Нет описания'
    if 'snippet' in json_item.keys():
        try:
            snippet = html2text.html2text(json_item['snippet']['requirement'])
        except AttributeError:
            snippet = 'Не указаны'
        responsibility = json_item['snippet']['responsibility']
    else:
        snippet = 'Не указаны'
        responsibility = 'Не указаны'
    url = json_item['alternate_url'] if json_item['alternate_url'] else "nope q_q"
    specs = ''
    if 'specializations' in json_item.keys():
        for spec in json_item['specializations']:
            specs += f"{spec['name']} - {spec['profarea_name']}\n"
    else:
        specs = 'Не указаны'
    result += f"{json_item['name']}\n\nЗП: {salary}\n\nКонтора: {employer}\n\nАдрес: {addres}\n\nТребования: {snippet}\n\nПроф области: {specs}\n\nОписание: {description}\n\nОбязанности: {responsibility}\n\nURL: {url}\n\n"
    return result


def parse_vacancy(json_resp):
    result = ""
    if json_resp:
        if 'items' in json_resp:
            json_resp = json_resp['items']
            for item in json_resp:
                yield parse_json(item)
        else:
            yield parse_json(json_resp)


if __name__ == '__main__':

    # print(next(get_random_vacancy()))
    # print(next(get_random_vacancy()))
    # print(parse_vacancy(get_random_vacancy()))

    for vac in get_vacancies_by_lang('java'):
        print(vac)
