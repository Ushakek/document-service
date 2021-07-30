from fastapi import APIRouter, File, UploadFile
from app.servies import create_pdf_report, create_html_report
from fastapi.responses import FileResponse

router = APIRouter()


@router.post('/get_html', response_class=FileResponse)
async def get_html_report(values: UploadFile = File(...), file: UploadFile = File(...)):
    html_template = await file.read()
    data = await values.read()
    report_html = create_html_report(template=html_template, values=data)
    return report_html


@router.post('/get_pdf', response_class=FileResponse)
async def get_pdf_report(values: UploadFile = File(...), file: UploadFile = File(...)):
    html_template = await file.read()
    data = await values.read()
    data = create_pdf_report(values=data, templates=html_template)
    return data
