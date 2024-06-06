import os
import mysql.connector.pooling

def create_db_pool():
    dbconfig = {
        "database": "spot",
        "user": "root",
        "password": os.environ['MYSQL_PASSWORD']
    }
    return mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **dbconfig)
