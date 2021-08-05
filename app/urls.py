from fastapi import APIRouter, UploadFile, Depends, HTTPException, Response
from app.servies import create_pdf_report, create_report
from app.dependencies import read_form
from fastapi.responses import FileResponse

router = APIRouter()


@router.put('/create_report', response_class=FileResponse)
def get_report(values: UploadFile = Depends(read_form)):

    data, template, convert_to = values
    extension = 'html' if template.filename.endswith('.html') else template.filename.split('.')[-1]
    media_type = template.content_type
    template = template.file.read()

    # Конвертирование строки в словарь, т.к. это переданный параметр.
    try:
        data = eval(data)
    except (SyntaxError, NameError):
        raise HTTPException(status_code=406, detail='Не верно передан словарь значений. Пожалуйста, посмотрите пример'
                                                    ' и повторите ещё раз.')

    if convert_to == 'pdf' and extension != 'html':
        message = 'Не удалось определить формат шаблона. Шаблон должен быть в формате html для конвертации в pdf'
        raise HTTPException(status_code=406, detail=message)
    elif convert_to == 'pdf' and extension == 'html':
        report = create_pdf_report(template=template, values=data)
        return Response(content=report, media_type='application/pdf')
    elif convert_to == 'default':
        report = create_report(template=template, values=data)
        return Response(content=report, media_type=media_type)
