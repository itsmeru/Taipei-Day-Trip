import os
import mysql.connector.pooling

def create_db_pool(db):
    dbconfig = {
        "host": os.environ.get("MYSQL_HOST", "localhost"),
        "user":"root",
        "database": db,
        "port":3306,
        "charset": "utf8mb4",
        "collation": "utf8mb4_unicode_ci",
        "password": os.environ.get("MYSQL_PASSWORD"),
    }
    return mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **dbconfig)
