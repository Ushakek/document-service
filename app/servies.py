from weasyprint import HTML
from datetime import datetime
from fastapi import Response, UploadFile, File, Form
from json import JSONDecoder


class SafeDict(dict):
    def __missing__(self, key):
        return 'Информация не найдена'


def create_report(template, values, media_type):
    """ Метод для автозаполнения документов

    Args:
        template: шаблон в любом формате, который в дальнейшем заполняется
        values: Значения, должны быть в виде словаря формата json
        media_type: тип документа

    Принимает в себя 2 значения  в битовом формате, дале производит декодирование этих значений. Далее заполняет
    отмеченные места в соответствии со значениями в словаре.

    Пример:
        template = 'Это новый {blank1}, который способен {blank2} пустые места'
        values = {'blank1': 'метод', 'blank2': 'заполнять'}
        return = 'Это новый метод, который способен заполнять пустые места'

    Returns:
        Response(): файл исходной кодировки или файл pdf
    """

    template = template.decode(encoding='utf8')
    values = values.decode(encoding='utf8')
    data = JSONDecoder().decode(values)

    current_date = datetime.now()
    date_sys = current_date.strftime('%Y.%m.%d')
    time_sys = current_date.strftime('%H:%M')
    date = data.get('date', date_sys)
    time = data.get('time', time_sys)

    filled_template = template.format_map(SafeDict(**data, date=date, time=time))
    return Response(content=filled_template, media_type=media_type)


def create_pdf_report(templates, values, media_type):
    html_report = create_report(template=templates, values=values, media_type=media_type)
    html_print = HTML(string=html_report.body)
    data = html_print.write_pdf()
    return Response(content=data, media_type='application/pdf')


async def common_parameters(values: UploadFile = File(...), file: UploadFile = File(...),
                            convert_to: str = Form('default', enum=['pdf'])):
    data = await values.read()
    template = await file.read()
    return data, template, file.content_type, convert_to
