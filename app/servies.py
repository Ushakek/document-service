from weasyprint import HTML
from datetime import datetime
from fastapi import Response

from app.editor_html import EditorHTML

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


def create_html_report(values):
    current_date = datetime.now()
    date = current_date.strftime('%Y.%m.%d')
    time = current_date.strftime('%H:%M')
    model = values.get('model', 'NO_NAME')
    group = values.get('group', 'NO_NAME')
    table_values = ''
    for idx, product in enumerate(values, 1):
        factory_number = values[product].get('adc_factory_number', '-')
        accuracy_value = values[product].get('Класс точности ИС', '-')
        accuracy_description = 'some value'  # Под вопросом
        temp_error_description = 'second some value'  # Под вопросом
        is_defective = values[product].get('defective')
        if is_defective:
            is_defective = 'Не годен'
            defective_report = values[product]['defective_report']
        else:
            is_defective = 'Годен'
            defective_report = '-'

        table_values += EditorHTML.fill_columns([idx, factory_number, accuracy_description,
                                                 temp_error_description, is_defective, defective_report])

    filled_template = HTML_REPORT.format(date=date, time=time, model=model, group=group, column_values=table_values)
    return Response(content=filled_template, media_type='application/html')


def create_pdf_report():
    html_print = HTML(string=HTML_REPORT)
    data = html_print.write_pdf()
    return Response(content=data, media_type='application/pdf', )
