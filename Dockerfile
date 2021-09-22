# Установка Ubuntu и python
FROM python:3.9-buster

# Обновление Ubuntu & Обновление pip и setuptools
RUN apt-get -y update \
    && apt-get install -y \
        fonts-font-awesome \
        libffi-dev \
        libgdk-pixbuf2.0-0 \
        libpango1.0-0 \
        python-dev \
        python-lxml \
        shared-mime-info \
        libcairo2 \
    && apt-get -y clean

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r ./requirements.txt

# Копирование run.py (запуск сервиса)
COPY run.py ./

# Копирование связанных файлов
COPY app ./app

CMD ["python", "-u", "run.py"]