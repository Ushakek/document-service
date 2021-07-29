import requests
from weasyprint import HTML
from fastapi import Response

HTML_REPORT = """
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


def report():
    html_print = HTML(string=HTML_REPORT)
    data = html_print.write_pdf()
    return Response(content=data, media_type='application/pdf', )
    # return html_print
