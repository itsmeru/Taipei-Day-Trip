import os
import mysql.connector.pooling

def create_db_pool(db):
    dbconfig = {
        "host": os.environ.get("MYSQL_HOST", "localhost"),
        "database": db,
        "password": os.environ.get("MYSQL_PASSWORD"),
    }
    return mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **dbconfig)
