FROM python:3.10

ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY crm .

CMD ["gunicorn", "crm.wsgi:application", "--bind", "0.0.0.0:8000"