FROM python:3.11.3

WORKDIR /greenthumbs

COPY . /greenthumbs

RUN python3 -m pip install -r /greenthumbs/requirements.txt

EXPOSE 5000

CMD [ "python3" ,  "/greenthumbs/app.py" ]