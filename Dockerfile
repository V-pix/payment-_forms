FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip

COPY requirements.txt .

COPY dump.json .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY payment_forms/ .

CMD ["python3", "manage.py", "runserver", "0:8000"] 
