FROM python:3.7

WORKDIR /opt
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8888

ENTRYPOINT ["python", "main.py"]