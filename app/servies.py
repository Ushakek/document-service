from weasyprint import HTML
from datetime import datetime


class SafeDict(dict):
    def __missing__(self, key):
        return 'Информация не найдена'


def create_report(template, values):
    """ Метод для автозаполнения документов

    Args:
        template: шаблон в любом формате и байтовом виде, который в дальнейшем заполняется
        values: Значения, должны быть в виде словаря

    Принимает в себя 2 значения  в битовом формате, дале производит декодирование этих значений. Далее заполняет
    отмеченные места в соответствии со значениями в словаре.

    Пример:
        template = 'Это новый {blank1}, который способен {blank2} пустые места'
        values = {'blank1': 'метод', 'blank2': 'заполнять'}
        return = 'Это новый метод, который способен заполнять пустые места'

    Returns:
        filled_template: заполненный файл
    """

    # Декодирование шаблона, т.к. передаётся в байтовом виде.
    template = template.decode(encoding='utf8')
    data = values

    current_date = datetime.now()

    if 'date' not in data.keys():
        data.update({'date': current_date.strftime('%Y.%m.%d')})

    if 'time' not in data.keys():
        data.update({'time': current_date.strftime('%H:%M')})

    filled_template = template.format_map(SafeDict(**data))
    return filled_template


def create_pdf_report(template, values):
    """ Метод конвертации HTML в PDF

    Использует метод create_report() для автозваполнения шаблона, передаёт этот шаблон в кодератор HTML5
    для дальнейшей конвертации в PDF. Можно использовать только HTML шаблоны

    Args:
        template: шаблон в формате HTML, который в дальнейшем заполняется
        values: Значения, должны быть в виде словаря

    Returns:
        data: Файл в формате pdf
    """
    html_report = create_report(template=template, values=values)
    html_print = HTML(string=html_report)
    data = html_print.write_pdf()
    return data

