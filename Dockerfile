FROM python:3.11.3

WORKDIR /project

COPY . /project

RUN python3 -m pip install -r /project/requirements.txt

EXPOSE 5000

CMD [ "python3" ,  "/project/app.py" ]