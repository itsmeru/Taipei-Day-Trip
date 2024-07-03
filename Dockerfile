# 第一階段：用於安裝依賴和構建
FROM python:3.9.7 AS builder

WORKDIR /usr/src/app

# 只複製依賴文件
COPY requirements.txt .

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 第二階段：用於生產環境運行
FROM python:3.9.7-slim

WORKDIR /usr/src/app

# 從第一階段複製安裝的依賴
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 複製项目文件
COPY . .

# 清理不必要的文件和缓存
RUN apt-get update && \
    apt-get install -y --no-install-recommends libgomp1 && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    find /usr/local/lib/python3.9/site-packages -type d -name '__pycache__' -exec rm -r {} +

# 暴露端口
EXPOSE 8000

# 啟動服務
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
