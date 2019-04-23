FROM python:3.7

ADD ./requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

RUN mkdir /earth_grid

ADD ./app/ /earth_grid/app/
ADD ./plugins /earth_grid/plugins/
ADD ./*.py /earth_grid/

WORKDIR /earth_grid

CMD ["python", "run_app.py"]