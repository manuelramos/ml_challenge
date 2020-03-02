# Use an official Python runtime as an image
FROM python:3.8

EXPOSE 5000
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY main.py database.py /app/
CMD python main.py