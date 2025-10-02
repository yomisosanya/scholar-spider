from util import search
from pathlib import Path
import psycopg as pg


def create_db(conn: pg.Connection, schema_path: str, dbname: str):
    with conn.cursor as cursor:
        with open(Path(schema_path), 'r') as f:
            cursor.execute('CREATE DATABASE {};'.format(dbname))
            cursor.execute(f.read())
        conn.commit()
    return


def insert_author():
    pass

def insert_paper():
    pass







