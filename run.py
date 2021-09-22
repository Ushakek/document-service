import uvicorn


def run():

    uvicorn.run('app.main:app', host='0.0.0.0', port=5051, reload=True)


if __name__ == '__main__':
    run()
