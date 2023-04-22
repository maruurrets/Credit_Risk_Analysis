FROM python:3.8.13 as base

ADD requirements.txt .
RUN pip3 install -r requirements.txt


ENV PYTHONPATH=$PYTHONPATH:/src/

ADD ./ /src/

WORKDIR /src

COPY train.py ./

CMD ["python3", "/src/train.py", "/src/pickles/X_train_prep.pickle", "/src/pickles/y_train.pickle"]


