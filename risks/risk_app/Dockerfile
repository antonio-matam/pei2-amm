FROM python:latest

RUN pip install --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY ./app /app 
WORKDIR /app
CMD ["python", "main.py"]


