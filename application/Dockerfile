FROM python:3.5.3
MAINTAINER Nicolas Huguenin "nichuguen@gmail.com"



WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

RUN python -m pip install -r /tmp/requirements.txt

WORKDIR /tmp

COPY WemIndexer-0.1.tar.gz package.tar.gz

RUN tar -xvf package.tar.gz && cd WemIndexer-0.1 && python setup.py install

WORKDIR /app

CMD ["python", "server.py"]
