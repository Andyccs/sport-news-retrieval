FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY crawler/requirements.txt /usr/src/app/crawler/
RUN pip install --no-cache-dir -r crawler/requirements.txt

COPY recrawler/requirements.txt /usr/src/app/recrawler/
RUN pip install --no-cache-dir -r recrawler/requirements.txt

RUN pip install --no-cache-dir -U numpy==1.10.4
RUN apt-get update && apt-get install -y --no-install-recommends \
    libatlas-base-dev \
    gfortran \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/ \
    && pip install --no-cache-dir scipy
RUN pip install --no-cache-dir scikit-learn

COPY crawler/ /usr/src/app/crawler/
COPY recrawler/ /usr/src/app/recrawler/

COPY classifier/__init__.py /usr/src/app/classifier/__init__.py
COPY classifier/classify_data.py /usr/src/app/classifier/classify_data.py
COPY model/ /usr/src/app/recrawler/model/

WORKDIR /usr/src/app/recrawler

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]