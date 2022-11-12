FROM python:3.10.8-slim-bullseye

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

CMD ["flask", "--app", "api", "run", "--host=0.0.0.0"]
