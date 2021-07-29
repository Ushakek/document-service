from fastapi import APIRouter
from app.servies import report
from fastapi.responses import HTMLResponse, FileResponse, Response

router = APIRouter()


@router.put('/get_pdf', response_class=FileResponse)
async def get_some():
    data = report()
    return data


