from weasyprint import HTML
from datetime import datetime


class SafeDict(dict):
    def __missing__(self, key):
        return key


def filling(template, values):
    """ Метод для автозаполнения документов

    Args:
        template: шаблон в который будет происходить заполнение из словаря values
        values: Значения, должны быть в виде словаря

    В метод принимается шаблон и значения, которые в дальнейшем заполняются.
    Если ключ в словаре есть, а в тексте нет - ничего не произойдёт. Если в тесте есть ключ, а в словаре нет -
    то ключ не заменится.

    Пример:
        template = 'Это новый {blank1}, который способен {blank2} пустые места'

        values = {'blank1': 'метод', 'blank2': 'заполнять'}

        return = 'Это новый метод, который способен заполнять пустые места'

    Returns:
        filled_template: заполненный шаблон
    """

    # Декодирование шаблона, т.к. передаётся в байтовом виде.
    data = values

    current_date = datetime.now()

    if not data.get('date'):
        data.update({'date': current_date.strftime('%Y.%m.%d')})

    if not data.get('time'):
        data.update({'time': current_date.strftime('%H:%M')})

    filled_template = template.format_map(SafeDict(**data))
    return filled_template


def converter_to_pdf(source):
    """ Метод конвертации HTML в PDF

    Использует weasyprint библиотеку для конвертации в PDF. Для того, что бы документ был правильно сконвертирован,
    исходный файл должен быть в формате HTML

    Args:
        source: шаблон в формате HTML, который в дальнейшем заполняется

    Returns:
        data: Файл в формате pdf
    """
    operation = HTML(string=source)
    data = operation.write_pdf()
    return data

