FROM python:3.12-alpine3.19


COPY ./requirements.txt /temp/requirements.txt
RUN mkdir bookabook
COPY ./backend /bookabook/backend
COPY ./.env /bookabook/.env
WORKDIR /bookabook/backend
EXPOSE 8000

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password frank

USER frank