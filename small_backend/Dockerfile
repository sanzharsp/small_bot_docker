FROM python:3.11.5

RUN apt-get update -y
RUN apt-get --fix-missing install
RUN apt-get upgrade -y

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./src ./src

CMD ["gunicorn", "-w", "4", "--chdir", "./src", "small.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "6000"]

