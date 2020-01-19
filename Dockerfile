FROM python:3.8-alpine

WORKDIR /src/

ADD demo /src/
RUN pip install --no-compile -r /src/requirements.txt && \
  chmod +x /src/boot.sh && \
  apk add --no-cache mariadb-client git && \
  adduser -D flask && \
  chown -R flask:flask /src/*

ENV FLASK_APP demo.py
ENV FLASK_DEBUG 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED TRUE

USER flask

EXPOSE 5000
ENTRYPOINT ["/src/boot.sh"]
