FROM python:alpine3.6

COPY requirements.txt /tmp/requirements.txt

RUN apk update \
  && apk --update add bash \
    bash-completion

RUN apk --update add --virtual build-dependencies \
    build-base \
  && apk --update add --no-cache postgresql-dev \
  && pip3 install --upgrade -r /tmp/requirements.txt \
  && pip3 install --upgrade nose \
    parameterized \
    mock \
    tox \
  && rm -rf /tmp/requirements.txt \
  && apk del build-dependencies