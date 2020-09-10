FROM python:3.8

WORKDIR /app
COPY ./ /app

RUN pip3 install -r requirements.txt

EXPOSE 80
CMD python3 tatshelter.py