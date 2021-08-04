from fastapi import APIRouter, UploadFile, Depends, HTTPException
from app.servies import create_pdf_report, create_report
from app.dependencies import read_form
from fastapi.responses import FileResponse

router = APIRouter()


@router.put('/create_report', response_class=FileResponse)
def get_report(values: UploadFile = Depends(read_form)):

    data, template, convert_to = values
    expansion = 'html' if template.filename.endswith('.html') else ''
    media_type = template.content_type
    template = template.file.read()
    try:
        data = eval(data)
    except (SyntaxError, NameError):
        raise HTTPException(status_code=406, detail='Не верно передан словарь значений. Пожалуйста, посмотрите пример'
                                                    ' и повторите ещё раз.')

    if convert_to == 'pdf' and expansion == '':
        message = 'Не удалось определить формат шаблона. Шаблон должен быть в формате html для конвертации в pdf'
        raise HTTPException(status_code=406, detail=message)
    elif convert_to == 'pdf' and expansion == 'html':
        report = create_pdf_report(template=template, values=data, media_type=media_type)
        return report
    elif convert_to == 'default':
        report = create_report(template=template, values=data, media_type=media_type)
        return report
