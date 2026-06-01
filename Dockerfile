FROM python:3.14 

WORKDIR /CODE

COPY ./requirements.txt /CODE/requirements.txt

RUN pip install --no-cache-dir -r /CODE/requirements.txt

COPY ./app /CODE/app

COPY ./alembic /CODE/alembic

COPY ./alembic.ini /CODE/alembic.ini

COPY ./start.sh /CODE/start.sh

CMD ["bash", "start.sh"]
