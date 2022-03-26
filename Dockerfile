FROM python:3

RUN apt-get update && apt-get install -y tzdata \
    libgdal-dev

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LD_LIBRARY_PATH=/usr/local/lib

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY app/tilkku/ /code/
