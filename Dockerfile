FROM python:alpine
MAINTAINER Lorenzo Carbonell <a.k.a. atareao>

ARG S6_OVERLAY_RELEASE=https://github.com/just-containers/s6-overlay/releases/latest/download/s6-overlay-amd64.tar.gz

ENV S6_OVERLAY_RELEASE=${S6_OVERLAY_RELEASE}
ENV PYTHONUNBUFFERED=1

ADD ${S6_OVERLAY_RELEASE} /tmp/s6overlay.tar.gz

RUN echo "**** install S6 ****" \
    apk upgrade --update --no-cache && \
    rm -rf /var/cache/apk/* && \
    tar xzf /tmp/s6overlay.tar.gz -C / &&\
    rm /tmp/s6overlay.tar.gz

COPY requirements.txt  /
RUN apk --update-cache add --virtual build-dependencies gcc libc-dev make && \
    pip install --no-cache-dir -r /requirements.txt && \
    apk del build-dependencies && \
    rm /requirements.txt

RUN addgroup user && \
    adduser -h /app -G user -D user && \
    mkdir -p /app/db && mkdir -p /app/config && \
    chown -R user:user /app

COPY ./etc /etc
COPY ./src/*.py /app/

VOLUME ["/app/db", "/app/config"]

WORKDIR /app

EXPOSE 8080

ENTRYPOINT ["/init"]
