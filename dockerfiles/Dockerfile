FROM python:alpine3.6

COPY requirements.txt /tmp/requirements.txt

RUN apk update \
  && apk --update add bash \
    bash-completion

RUN apk --update add --virtual build-dependencies \
    build-base \
  && pip3 install --upgrade -r /tmp/requirements.txt \
  && rm -rf /tmp/requirements.txt \
  && apk del build-dependencies

COPY ['berkshire', ]
