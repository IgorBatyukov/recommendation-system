FROM python:3.10-slim

ARG SERVICE_NAME
ENV SERVICE_NAME=${SERVICE_NAME}

ENV WORK_DIR=/opt
ENV PYTHONPATH=${WORK_DIR}

WORKDIR ${WORK_DIR}

COPY services/${SERVICE_NAME} services/${SERVICE_NAME}
COPY services/resources services/resources

RUN pip install --no-cache-dir -r services/${SERVICE_NAME}/requirements.txt

ENTRYPOINT ["sh", "-c", "python services/${SERVICE_NAME}/src/main.py"]
