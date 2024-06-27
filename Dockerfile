# 第一階段：用於安裝依賴和構建
FROM python:3.9.7 AS builder

WORKDIR /usr/src/app

# 只复制依赖文件
COPY requirements.txt .

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 第二階段：用於生產環境運行
FROM python:3.9.7-slim

WORKDIR /usr/src/app

# 從第一階段複製安裝的依賴
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 8000

# 啟動服務
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
