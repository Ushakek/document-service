# Установка Ubuntu и python
FROM python:3.8-slim-buster

# Обновление Ubuntu & Обновление pip и setuptools
RUN apt-get -y update \
    && apt-get -y upgrade \
    && python -m pip install --upgrade pip setuptools \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r ./requirements.txt

# Копирование run.py (запуск сервиса)
COPY run.py ./

# Копирование связанных файлов
COPY app ./app

CMD ["python", "-u", "run.py"]