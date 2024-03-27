FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /server

COPY api/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "api/manage.py", "runserver", "0.0.0.0:8000"]