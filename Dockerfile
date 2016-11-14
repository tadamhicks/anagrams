FROM python:2.7-slim

MAINTAINER Adam Hicks <thomas.adam.hicks@gmail.com>

ENV INSTALL_PATH /endpoint

RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

RUN pip install Flask && \
    pip install numpy

COPY . .

EXPOSE 3000

CMD ["python", "./endpoint.py"]
