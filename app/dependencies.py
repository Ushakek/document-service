from fastapi import UploadFile, File, Query
from pydantic import BaseModel, Field


class Items(BaseModel):
    val: dict = Field(..., title='Подставляемые значения')


def read_form(values: UploadFile = File(...),
              file: UploadFile = File(...),
              convert_to: str = Query(default='default', enum=['pdf'])):

    data = values.file.read()
    template = file.file.read()
    return data, template, file.content_type, convert_to
