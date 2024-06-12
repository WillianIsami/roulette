FROM python:3.10

WORKDIR /opt/server

COPY . .

RUN pip install -r api/requirements.txt

RUN chmod +x /opt/server/entrypoint.sh
ENTRYPOINT ["/opt/server/entrypoint.sh"]

EXPOSE 8080

CMD ["python3", "api/manage.py", "runserver"]