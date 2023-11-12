import services.secrets as os
import mysql.connector
import logging
from time import sleep

logging.basicConfig(level=logging.INFO)

MAIN_DATABASE = os.getenv("DB_MAIN_DATABASE")
HOST_PUBLIC = os.getenv("DB_HOST_PUBLIC")
HOST_PRIVATE = os.getenv("DB_HOST_PRIVATE")

dbConnection = None
dbCursor = None


def connect_db(user: str = None, password: str = None) -> None:
    from multiprocessing import Process

    global dbConnection, dbCursor

    def connection(host: str = "private"):
        global dbConnection, dbCursor
        if host == "private":
            host = HOST_PRIVATE
        elif host == "public":
            host = HOST_PUBLIC

        dbConnection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=MAIN_DATABASE,
            ssl_disabled=True,
        )

        dbCursor = dbConnection.cursor()

    hostStr = "private"
    connect = Process(target=connection, args=(hostStr,))
    connect.start()

    sleep(15)
    if dbConnection is None:
        connect.kill()
        connection(host="public")

    elif hasattr(dbConnection, "is_connected"):
        if not dbConnection.is_connected():
            connect.kill()
            connection(host="public")


def disconnect_db() -> None:
    """a"""
    dbCursor.close()
    dbConnection.close()


def dbConnectionVerify(func):
    def wrapper(*args, **kwargs):
        if not hasattr(dbConnection, "is_connected"):
            connect_db(os.getenv("DB_SP_LOGIN"), os.getenv("SP_CONNECT_KEY"))

        else:
            connected = dbConnection.is_connected()
            if not connected:
                connect_db(os.getenv("DB_SP_LOGIN"), os.getenv("SP_CONNECT_KEY"))

        result = func(*args, **kwargs)
        return result

    wrapper.__name__ = func.__name__
    return wrapper


@dbConnectionVerify
def executar_comando_sql(sql: str, values=None):
    """a"""
    try:
        if values is None:
            dbCursor.execute(sql)

        elif values is not None:
            dbCursor.execute(sql, values)

        if "SELECT" in sql or "select" in sql:
            result = dbCursor.fetchall()
            dbConnection.commit()
            return result

        dbConnection.commit()

    except Exception as e:
        logging.error(e)
        pass
