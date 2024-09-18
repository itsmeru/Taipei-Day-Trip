FROM python:3.9.7 AS builder

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9.7-slim

WORKDIR /usr/src/app

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

RUN apt-get update && \
    apt-get install -y --no-install-recommends libgomp1 && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    find /usr/local/lib/python3.9/site-packages -type d -name '__pycache__' -exec rm -r {} +


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
