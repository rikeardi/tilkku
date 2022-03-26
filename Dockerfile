FROM python:3

RUN apt-get install -y libgdal-dev g++ --no-install-recommends && \
    apt-get clean -y

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LD_LIBRARY_PATH=/usr/local/lib

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY app/tilkku/ /code/
