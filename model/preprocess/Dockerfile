FROM python:3.8.13 as base

ADD requirements.txt .
RUN pip3 install -r requirements.txt


ENV PYTHONPATH=$PYTHONPATH:/src/

ADD ./ /src/

WORKDIR /src

COPY preprocess.py ./

CMD ["python3", "/src/preprocess.py", "/src/data/PAKDD2010_Modeling_Data.txt"]


