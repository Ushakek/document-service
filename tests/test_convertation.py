from app.main import app
from fastapi.testclient import TestClient
import json

client = TestClient(app)


# Проверка на конвертацию в оригинальный формат
def test_convert_to_original():
    with open('_data/_reference/reference_report.html', 'rb') as file:
        reference = file.read()

    with open('_data/_source/data_to_report.json', 'r') as file:
        values = file.read()

    params = {'values': values}

    response = client.put(url='/create_report',
                          files=[('template', open('_data/_source/verification.html', 'rb'))],
                          params=params)

    with open('_data/_current/report_html.html', 'wb') as file:
        file.write(response.content)

    assert response.status_code == 200
    assert response.content == reference
    print('\nЕсли тест пройден, файл записан, его можно посмотреть для проверки наполнения')


# Проверка на конвертацию в pdf
def test_convert_to_pdf():
    with open('_data/_source/data_to_report.json', 'r') as file:
        values = file.read()

    params = {'convert_to': 'pdf', 'values': values}

    response = client.put('/create_report?convert_to=pdf',
                          files=[('template', open('_data/_source/verification.html', 'rb'))],
                          params=params)

    assert response.status_code == 200

    with open('_data/_current/report_pdf.pdf', 'wb') as file:
        file.write(response.content)
    print('\nЕсли тест пройден, файл записан, его можно посмотреть для проверки наполнения')


# Проверка на ошибку при конвертации в связи с неверно переданными параметрами
def test_error_converting():
    with open('_data/_source/data_to_report.json', 'r') as file:
        values = file.read()

    params = {'convert_to': 'pdf', 'values': values}

    response = client.put('/create_report?convert_to=pdf',
                          files=[('template', open('_data/_source/test.txt', 'rb'))],
                          params=params)

    assert response.status_code == 406
    message = {'detail': 'Не удалось определить формат шаблона. Шаблон должен быть в формате html для конвертации в pdf'}
    assert response.json() == message


# Проверка возможности конвертации в шаблон НЕ HTML
def test_convert_to_any_template():
    with open('_data/_source/data_to_report.json', 'r') as file:
        values = file.read()

    params = {'values': values}

    with open('_data/_reference/reference_any.txt', 'rb') as file:
        reference = file.read()
    response = client.put('/create_report?convert_to=default',
                          files=[('template', open('_data/_source/test.txt', 'rb'))],
                          params=params)

    assert response.status_code == 200
    assert reference == response.content

    with open('_data/_current/report_any.txt', 'wb') as file:
        file.write(response.content)

    print('\nЕсли тест пройден, файл записан, его можно посмотреть для проверки наполнения')


# Проверка на ошибку при конвертации, если записаны неверные значения
def test_not_valid_values():
    values = 'some not valid string'
    params = {'values': values}

    response = client.put('/create_report?convert_to=pdf',
                          files=[('template', open('_data/_source/test.txt', 'rb'))],
                          params=params)

    assert response.status_code == 406
    message = {
        'detail': 'Не верно передан словарь значений. Пожалуйста, посмотрите пример'
                  ' и повторите ещё раз.'}
    assert response.json() == message


# Проверка на возможность конвертации после кодировки json
def test_json_format():
    dict_values = {
   "column_values": "<tr><td>1</td><td>12345</td><td>some value</td><td>second some value</td><td>Годен</td><td>-</td></tr><tr><td>2</td><td>123456</td><td>some value</td><td>second some value</td><td>Не годен</td><td>Потому что потому, всё кончается на 'У'!</td></tr>",
    "model": "Smart_S",
    "date": "date now",
    "time": "time now"
 }

    values = json.dumps(dict_values)

    params = {'values': values}

    response = client.put('/create_report?convert_to=pdf',
                          files=[('template', open('_data/_source/verification.html', 'rb'))],
                          params=params)

    with open('_data/_current/report_from_json.pdf', 'wb') as file:
        file.write(response.content)

    assert response.status_code == 200


# Проверка на ошибку конвертации при использовании не верного формата передачи в requests
def test_transit_dict():
    dict_values = {
        "column_values": "<tr><td>1</td><td>12345</td><td>some value</td><td>second some value</td><td>Годен</td><td>-</td></tr><tr><td>2</td><td>123456</td><td>some value</td><td>second some value</td><td>Не годен</td><td>Потому что потому, всё кончается на 'У'!</td></tr>",
        "model": "Smart_S",
        "date": "date now",
        "time": "time now"
    }

    params = {'values': dict_values}

    response = client.put('/create_report?convert_to=pdf',
                          files=[('template', open('_data/_source/verification.html', 'rb'))],
                          params=params)

    message = {
        'detail': 'Не верно передан словарь значений. Пожалуйста, посмотрите пример'
                  ' и повторите ещё раз.'}

    assert response.status_code == 406
    assert response.json() == message
