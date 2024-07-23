import os
import mysql.connector.pooling
import redis

def create_db_pool(db):
    dbconfig = {
        "host": os.environ.get("RDS_HOST", "localhost"),
        "user":os.environ.get("RDS_USER", "root"),
        "database": db,
        "port":3306,
        "password": os.environ.get("RDS_PASSWORD"),
    }
    return mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **dbconfig)

# def create_db_pool(db):
#     dbconfig = {
#         "host": "localhost",
#         "user": "root",
#         "database": db,
#         "port":3306,
#         "password": os.environ.get("MYSQL_PASSWORD"),
#     }
#     return mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **dbconfig)


def get_redis_connection():
    return redis.StrictRedis(host="redis", port=6379, db=0)
