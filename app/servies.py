from weasyprint import HTML
from datetime import datetime
from fastapi import Response
from json import JSONDecoder


class SafeDict(dict):
    def __missing__(self, key):
        return 'Информация не найдена'


def create_html_report(template, values):

    template = template.decode(encoding='utf8')
    values = values.decode(encoding='utf8')
    data = JSONDecoder().decode(values)

    current_date = datetime.now()
    date_sys = current_date.strftime('%Y.%m.%d')
    time_sys = current_date.strftime('%H:%M')
    date = data.get('date', date_sys)
    time = data.get('time', time_sys)

    filled_template = template.format_map(SafeDict(**data, date=date, time=time))
    return Response(content=filled_template, media_type='application/html')


def create_pdf_report(templates, values):
    html_report = create_html_report(template=templates, values=values)
    html_print = HTML(string=html_report.body)
    data = html_print.write_pdf()
    return Response(content=data, media_type='application/pdf')
