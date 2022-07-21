FROM python:3

RUN apt-get update && apt-get install -y tzdata \
    libgdal-dev g++ gettext

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LD_LIBRARY_PATH=/usr/local/lib
ENV DJANGO_SETTINGS_MODULE=tilkku.settings
ENV DJANGO_ALLOW_ASYNC_UNSAFE=1

WORKDIR /code
COPY requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./runserver.sh /code/

RUN chmod +x runserver.sh
CMD ["/code/runserver.sh"]
