FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y build-essential unzip curl python3-pip python3-dev python3-matplotlib \
    python3-lxml python3-numpy python3-dateutil python3-gdal python3-yaml python3-serial python3-shapely \
    python3-pil python3-reportlab python3-reportlab-accel python3-xlrd ansible git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install selenium>=2.23.0 sunburnt>=0.6 TwitterSearch>=1.0 requests>=2.3.0 xlwt

RUN curl -L -o web2py.zip https://github.com/web2py/web2py/archive/refs/tags/2.19.1.zip && \
    unzip web2py.zip && mv web2py-2.19.1 /home/web2py && rm web2py.zip

RUN pip3 install pydal yatl

COPY . /home/web2py/applications/eden

RUN cp /home/web2py/applications/eden/modules/templates/000_config.py /home/web2py/applications/eden/models/000_config.py && sed -i 's|EDITING_CONFIG_FILE = False|EDITING_CONFIG_FILE = True|' /home/web2py/applications/eden/models/000_config.py

CMD python3 /home/web2py/web2py.py -i 0.0.0.0 -p 8000 -a eden