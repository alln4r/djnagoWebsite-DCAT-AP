FROM python:3.7.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

copy requirements.txt /code/

RUN pip install --user -r requirements.txt

copy . /code/

CMD python manage.py runserver 0.0.0.0:8000