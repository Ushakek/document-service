from pathlib import Path
from unittest import TestCase
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

HTML = """
<!DOCTYPE html>
<html lang="rus">
<meta charset="UTF-8">
<style>
    html {
        background-color: #FFFFFF;
    }
    p{
        font-family: "Liberation Serif";
        font-size: 10pt;
        text-align: right;
    }
    table, th, td {
        font-family: "Liberation Serif";
        font-size: 10pt;
        border: 1px solid black;
        border-collapse: collapse;
    }
    caption{
        text-align: center;
    }
    th {
        text-align: left;
    }
    td {
        text-align: center;
        vertical-align: middle;
    }
</style>

<head>
    <title>Отчет Физ.Верификация</title>
</head>

<body>
<p>
    <b>Дата:</b> date now <b>Время:</b> time now <br>
    <b>Модель:</b> Smart_S <br>
    <b>Партия:</b> Информация не найдена
</p>

<table>
    <caption>Протокол Физической Верификации</caption>
<!--    HEADER-->
    <thead>
        <tr>
            <th style="text-align: center">№</th>
            <th style="text-align: center">Зав.Номер</th>
            <th style="text-align: center">Класс точности</th>
            <th style="text-align: center">Код темп.диапазона</th>
            <th style="text-align: center">Годность</th>
            <th style="text-align: center">Причина брака</th>
        </tr>
    </thead>
    <tbody>
    <tr><td>1</td><td>12345</td><td>some value</td><td>second some value</td><td>Годен</td><td>-</td></tr><tr><td>2</td><td>123456</td><td>some value</td><td>second some value</td><td>Не годен</td><td>Потому что потому, всё кончается на 'У'!</td></tr>
    </tbody>


</table>
</body>
"""
DATA = """
{
   "column_values": "<tr><td>1</td><td>12345</td><td>some value</td><td>second some value</td><td>Годен</td><td>-</td></tr><tr><td>2</td><td>123456</td><td>some value</td><td>second some value</td><td>Не годен</td><td>Потому что потому, всё кончается на 'У'!</td></tr>",   
    "model": "Smart_S",
    "date": "date now",
    "time": "time now"
 }
"""
EMPTY_HTML = """
<!DOCTYPE html>
<html lang="rus">
<meta charset="UTF-8">
<style>
    html {{
        background-color: #FFFFFF;
    }}
    p{{
        font-family: "Liberation Serif";
        font-size: 10pt;
        text-align: right;
    }}
    table, th, td {{
        font-family: "Liberation Serif";
        font-size: 10pt;
        border: 1px solid black;
        border-collapse: collapse;
    }}
    caption{{
        text-align: center;
    }}
    th {{
        text-align: left;
    }}
    td {{
        text-align: center;
        vertical-align: middle;
    }}
</style>

<head>
    <title>Отчет Физ.Верификация</title>
</head>

<body>
<p>
    <b>Дата:</b> {date} <b>Время:</b> {time} <br>
    <b>Модель:</b> {model} <br>
    <b>Партия:</b> {group}
</p>

<table>
    <caption>Протокол Физической Верификации</caption>
<!--    HEADER-->
    <thead>
        <tr>
            <th style="text-align: center">№</th>
            <th style="text-align: center">Зав.Номер</th>
            <th style="text-align: center">Класс точности</th>
            <th style="text-align: center">Код темп.диапазона</th>
            <th style="text-align: center">Годность</th>
            <th style="text-align: center">Причина брака</th>
        </tr>
    </thead>
    <tbody>
    {column_values}
    </tbody>


</table>
</body>

"""


class TestService(TestCase):

    # Создание файлов для теста
    def setUp(self) -> None:
        if not Path('_data').exists():
            parent = Path.cwd() / '_data'
            Path.mkdir(parent)

            with open(f'{parent}/reference.html', 'w') as file:
                file.write(HTML)
            with open(f'{parent}/empty.html', 'w') as file:
                file.write(EMPTY_HTML)
            with open(f'{parent}/data.txt', 'w') as file:
                file.write(DATA)

    # Проверка на подстановку в файл
    def test_filling(self):
        with open('_data/reference.html', 'rb') as file:
            reference = file.read()
        with open('_data/data.txt', 'r') as file:
            values = file.read()

        params = {'data': values}

        response = client.put(url='/filing_template',
                              files=[('template', open('_data/empty.html', 'rb'))],
                              params=params)

        assert response.status_code == 200
        assert reference == response.content

    # Проверка на конвертацию в pdf
    def test_convert_to_pdf(self):
        response = client.put('/converter',
                              files=[('template', open('_data/reference.html', 'rb'))])

        assert response.status_code == 200

        with open(Path.cwd() / 'converted.pdf', 'wb') as file:
            file.write(response.content)

        self.assertTrue(Path('converted.pdf').exists())
        Path('converted.pdf').unlink()
