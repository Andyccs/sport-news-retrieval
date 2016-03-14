FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY crawler/requirements.txt /usr/src/app/crawler/
RUN pip install --no-cache-dir -r crawler/requirements.txt

COPY recrawler/requirements.txt /usr/src/app/recrawler/
RUN pip install --no-cache-dir -r recrawler/requirements.txt

COPY crawler/ /usr/src/app/crawler/
COPY recrawler/ /usr/src/app/recrawler/

WORKDIR /usr/src/app/recrawler

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]