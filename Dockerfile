FROM python:3.11-slim

ARG SERVICE_NAME
ENV SERVICE_NAME=${SERVICE_NAME}

ENV WORK_DIR=/opt
ENV PYTHONPATH=${WORK_DIR}

WORKDIR ${WORK_DIR}

COPY services/${SERVICE_NAME} services/${SERVICE_NAME}
COPY resources resources

RUN pip install --no-cache-dir -r services/${SERVICE_NAME}/requirements.txt

ENTRYPOINT ["sh", "-c", "python services/${SERVICE_NAME}/src/main.py"]
