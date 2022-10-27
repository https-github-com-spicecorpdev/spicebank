import sys
import mariadb

def connect():
    try:
        connection = mariadb.connect(
            user="root",
            password="123456",
            host="127.0.0.1",
            port=3308,
            database = "spicebank"
        )
        connection.auto_reconnect = True
    except mariadb.Error as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)
    return connection

def connection_pool():
    pool = mariadb.ConnectionPool(
            user="root",
            password="123456",
            host="127.0.0.1",
            port=3308,
            database = "spicebank",
            pool_name="spicebank",
            pool_size=20
        )
    return pool