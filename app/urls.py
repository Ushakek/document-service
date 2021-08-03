from fastapi import APIRouter, UploadFile, Depends
from app.servies import create_pdf_report, create_report, common_parameters
from fastapi.responses import FileResponse

router = APIRouter()


@router.put('/create_report', response_class=FileResponse)
def get_report(values: UploadFile = Depends(common_parameters)):
    data, html_template, media_type, convert_to = values

    if convert_to == 'default' or media_type != 'text/html':
        report = create_report(template=html_template, values=data, media_type=media_type)
        return report
    elif convert_to == 'pdf' and media_type == 'text/html':
        report = create_pdf_report(templates=html_template, values=data, media_type=media_type)
        return report
