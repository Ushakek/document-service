from fastapi import APIRouter
from app.servies import create_pdf_report, create_html_report
from fastapi.responses import HTMLResponse, FileResponse, Response

router = APIRouter()


@router.put('/html_report', response_class=FileResponse)
async def get_html_report(values: dict):
    data = create_html_report(values)
    return data


@router.get('/help')
def help_me():
    return {'some': {'data': 'in data'}, 'next_some': {'data': 'next: data'}}


@router.get('/get_pdf', response_class=FileResponse)
async def get_pdf_report():
    data = create_pdf_report()
    return data


