from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_convert_to_original():
    with open('_data/_reference/reference_report.html', 'rb') as file:
        reference = file.read()

    response = client.put('/create_report?convert_to=default',
                          files=[('values', open('_data/_source/data_to_report.json', 'rb')),
                                 ('file', open('_data/_source/verification.html', 'rb'))])

    with open('_data/_current/report_html.html', 'wb') as file:
        file.write(response.content)

    assert response.status_code == 200
    assert response.content == reference
    print('\nЕсли тест пройден, файл записан, его можно посмотреть для проверки наполнения')


def test_convert_to_pdf():
    response = client.put('/create_report?convert_to=pdf',
                          files=[('values', open('_data/_source/data_to_report.json', 'rb')),
                                 ('file', open('_data/_source/verification.html', 'rb'))])

    assert response.status_code == 200

    with open('_data/_current/report_pdf.pdf', 'wb') as file:
        file.write(response.content)
    print('\nЕсли тест пройден, файл записан, его можно посмотреть для проверки наполнения')


def test_error_converting():
    response = client.put('/create_report?convert_to=pdf',
                          files=[('values', open('_data/_source/data_to_report.json', 'rb')),
                                 ('file', open('_data/_source/test.txt', 'rb'))])

    assert response.status_code == 406
    message = {'detail': 'Не удалось определить формат шаблона. Шаблон должен быть в формате html для конвертации в pdf'}
    assert response.json() == message


def test_convert_to_any_template():
    with open('_data/_reference/reference_any.txt', 'rb') as file:
        reference = file.read()
    response = client.put('/create_report?convert_to=default',
                          files=[('values', open('_data/_source/data_to_report.json', 'rb')),
                                 ('file', open('_data/_source/test.txt', 'rb'))])

    assert response.status_code == 200
    assert reference == response.content

    with open('_data/_current/report_any.txt', 'wb') as file:
        file.write(response.content)

    print('\nЕсли тест пройден, файл записан, его можно посмотреть для проверки наполнения')


def test_any_format_data():
    with open('_data/_reference/reference_any_data.txt', 'rb') as file:
        reference = file.read()

    response = client.put('/create_report?convert_to=default',
                          files=[('values', open('_data/_source/data_to_report.txt', 'rb')),
                                 ('file', open('_data/_source/test.txt', 'rb'))])

    assert response.status_code == 200
    assert reference == response.content

    with open('_data/_current/report_any_data.txt', 'wb') as file:
        file.write(response.content)
