FROM python:alpine

RUN pip install flask-restful jsonpickle

COPY . /article_api

WORKDIR /article_api

EXPOSE 5000

CMD ["python3", "api.py"]
