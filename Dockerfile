FROM python:3.9.7


WORKDIR /user/src/app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y mysql-client && \
    rm -rf /var/lib/apt/lists/*
    
EXPOSE 8000
# ENV ABC=123
# ENV MYSQL_HOST=mydb
# ENV MYSQL_PORT=3306
# ENV MYSQL_USER=root
# ENV MYSQL_PASSWORD=betty520

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["/bin/bash"]