FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/services/flaskapp/src

COPY requirements.txt /opt/services/flaskapp/src/

WORKDIR /opt/services/flaskapp/src

RUN pip install -r requirements.txt

COPY . /opt/services/flaskapp/src

EXPOSE 5000

CMD ["python", "server.py"]