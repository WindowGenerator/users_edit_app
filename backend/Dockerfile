FROM python:3.9.10-bullseye

ENV WORK_DIR /opt/app
WORKDIR ${WORK_DIR}

COPY src ${WORK_DIR}/src
COPY requirements.txt ${WORK_DIR}/requirements.txt

RUN python3 -m pip install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0",  "--port", "1337", "--reload"]