from fastapi import UploadFile, File, Query


def read_form(values: str = Query(..., description='Значения для подстановки в файл. '
                                                   'Данные должны быть в формате словаря.',
                                  example={'first key': 'fist data'}),
              template: UploadFile = File(..., description='Шаблон в который подставляются значения из `values`.'
                                                           ' Должен содержать `{<ключ>}`, для успешной подстановки, '
                                                           'где `<ключ>`, совпадает с ключами '
                                                           'передаваемого словаря `values`.'),
              convert_to: str = Query(default='default', enum=['pdf'],
                                      description='Формат файла после конвертации. '
                                                  'Значение по умолчанию - конвертация в формат шаблона.'
                                                  '<br>`WARING`: Конвертация в формат pdf возможна только, если шаблон '
                                                  'в формате html.')):

    return values, template, convert_to
