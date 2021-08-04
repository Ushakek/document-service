from fastapi import UploadFile, File, Query


def read_form(values: UploadFile = File(...),
              file: UploadFile = File(...),
              convert_to: str = Query(default='default', enum=['pdf'])):

    expansion = 'html' if '.html' in file.filename else ''
    data = values.file.read()
    template = file.file.read()
    return data, template, file.content_type, expansion, convert_to
