FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LD_LIBRARY_PATH=/usr/local/lib
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY app/tilkku/ /code/
