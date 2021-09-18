from fastapi import APIRouter, UploadFile, HTTPException, Response, Query, File
from app.logic import filling, converter_to_pdf
from json import loads, JSONDecodeError

router = APIRouter()


@router.put('/filing_template')
def filling_template(data: str = Query(..., description='Значения для подстановки в файл. '
                                                        'Данные должны быть в формате словаря.',
                                       example={'first key': 'fist data'}),
                     template: UploadFile = File(...,
                                                 description='Шаблон в который подставляются значения из `values`.'
                                                             ' Должен содержать `{<ключ>}`, для успешной подстановки, '
                                                             'где `<ключ>`, совпадает с ключами '
                                                             'передаваемого словаря `values`.')):

    media_type = template.content_type
    template = template.file.read()
    template = template.decode(encoding='utf8')

    # Конвертирование строки в словарь, т.к. это переданный параметр.
    try:
        data = loads(data)
    except (TypeError, JSONDecodeError):
        raise HTTPException(status_code=406, detail='Не верно передан словарь значений. Пожалуйста, посмотрите пример'
                                                    ' и повторите ещё раз.')

    op = filling(template=template, values=data)
    return Response(content=op, media_type=media_type)


@router.put('/converter')
def converter(template: UploadFile = File(..., description='Шаблон, который будет сконвртирован в `PDF`.'
                                                           'Для успешной конвертации нужно использовать `HTML` шаблон')):

    template = template.file.read()
    op = converter_to_pdf(template)
    return Response(content=op, media_type='application/pdf')
