ARG PY_BASE_IMAGE=docker.m.daocloud.io/library/python:3.12-slim
FROM ${PY_BASE_IMAGE}

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
