FROM python:3.8-alpine

WORKDIR /src/

ADD demo /src/
RUN pip install -r /src/requirements.txt
RUN chmod +x /src/boot.sh
RUN apk add mariadb-client git

ENV FLASK_APP demo.py
ENV FLASK_DEBUG 1

EXPOSE 5000
ENTRYPOINT ["/src/boot.sh"]
