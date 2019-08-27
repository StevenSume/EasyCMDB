FROM docker.io/python:3.7
ADD ./requirement.txt /
RUN pip install -r requirement.txt
ADD . /
EXPOSE 5000
WORKDIR /
CMD python run.py runserver -h 0.0.0.0
