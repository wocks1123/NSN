FROM python:3.10

WORKDIR /workspace

COPY . /workspace

RUN pip install --no-cache-dir --upgrade -r /workspace/requirements.txt
