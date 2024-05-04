FROM python:3.10-bookworm

WORKDIR /workspace

COPY gen2rec gen2rec
COPY requirements.txt .
COPY news.csv news.csv

RUN python -m pip install uv && uv venv && uv pip install -r requirements.txt

ENTRYPOINT ["/bin/bash"]
