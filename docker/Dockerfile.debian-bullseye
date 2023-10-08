FROM debian:bullseye

RUN apt-get update
RUN apt-get install -y \
	python3-clang \
	python3-venv \
	make
RUN apt-get clean

ARG UID=1000
ARG GID=1000
ARG ARCHIVE

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD ${ARCHIVE} .

RUN sh venv

ENV PATH=".venv/bin:${PATH}"

USER ${UID}:${GID}
