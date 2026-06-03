FROM python:3.12-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

EXPOSE 8000

COPY ./app /code/app

COPY ./alembic /code/alembic

COPY ./alembic.ini /code/alembic.ini

COPY ./start.sh /code/start.sh

CMD ["bash", "start.sh"]
