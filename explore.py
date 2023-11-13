import numpy as np
import interface
import psycopg2
import itertools
from typing import TypedDict, List


class LoginDetails(TypedDict):
    host: str
    port: int
    user: str
    password: str


class QueryDetails(TypedDict):
    database: str
    query: str

class DatabaseConnector(object):
    """
    psycopg2 connector to the postgresql database
    """

    def __init__(self, login_details: LoginDetails, dbname=None):
        if dbname is None:
            self.connector = psycopg2.connect(host=login_details.host, port=login_details.port,
                                              user=login_details.user, password=login_details.password).cursor()
        else:
            self.connector = psycopg2.connect(host=login_details.host, port=login_details.port,
                                              user=login_details.user, password=login_details.password,
                                              dbname=dbname).cursor()

    def __enter__(self):
        return self.connector

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connector.close()

def get_database_names(login_details: LoginDetails) -> List[str]:
    """
    Retrieve list of databases
    """
    try:
        with DatabaseConnector(login_details) as cursor:
            query = "SELECT datname FROM pg_database WHERE datistemplate = false;"
            cursor.execute(query)
            database_list = cursor.fetchall()
            database_list = [i[0] for i in database_list]
            return database_list
    except psycopg2.OperationalError as e:
        Main.show_error(str(e))


def get_tables_in_database(login_details: LoginDetails, db: str) -> List[str]:
    """
    Retrieve list of tables in specified database
    """
    try:
        with DatabaseConnector(login_details, db) as cursor:
            query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
            cursor.execute(query)
            table_list = cursor.fetchall()
            table_list = [i[0] for i in table_list]
            return table_list
    except psycopg2.OperationalError as e:
        main.show_error(str(e))


def get_columns_for_table(login_details: LoginDetails, db: str, schema: str) -> List[str]:
    """
    Get list of columns present in a given table.
    """
    try:
        with DatabaseConnector(login_details, db) as cursor:
            query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{schema}' AND table_catalog = '{db}';"
            cursor.execute(query)
            res = cursor.fetchall()
            res = [_[0] for _ in res]
            return res
    except psycopg2.OperationalError as e:
        from project import Main
        Main.show_error(str(e))
