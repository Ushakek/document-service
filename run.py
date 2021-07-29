import os
import uvicorn


def run():
    reload = os.environ.get('EQUIPMENT_SERVICE_RELOAD') is None
    host = '0.0.0.0' if not reload else '127.0.0.1'

    uvicorn.run('app.main:app', host=host, port=12345, reload=reload)


if __name__ == '__main__':
    run()
