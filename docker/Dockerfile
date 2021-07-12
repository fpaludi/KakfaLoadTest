FROM python:3.8.5-slim-buster

RUN apt-get update --fix-missing -y && \
    apt-get install -y gcc

WORKDIR /workspace/
COPY requirements/requirements.txt ./
COPY requirements/test_requirements.txt ./
RUN pip install -r requirements.txt
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pip install -r test_requirements.txt ; fi"
COPY ./src/ ./

CMD ["python", "main.py"]
