FROM python:3.10.13-slim-bullseye

ENV PROJECT="/opt/service"
RUN mkdir -p ${PROJECT}
WORKDIR ${PROJECT}
RUN mkdir -p ${PROJECT}/notebooks
RUN mkdir -p ${PROJECT}/input

COPY docker/python_requirements.txt ${PROJECT}

RUN pip install --no-cache-dir -r python_requirements.txt

