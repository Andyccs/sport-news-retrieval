FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY crawler/ /usr/src/app/crawler/
COPY recrawler/ /usr/src/app/recrawler/

# RUN apt-get update && apt-get install -y \
#     gcc \
#     gettext \
#     mysql-client libmysqlclient-dev \
#     postgresql-client libpq-dev \
#     sqlite3 \
#   --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app/recrawler

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]