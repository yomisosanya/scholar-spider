from util import search
from pathlib import Path
import psycopg as pg


def create_db(conn: pg.Connection, dbname: str, schema_path: str = 'schema.sql'):
    with conn.cursor as cursor:
        with open(Path(schema_path), 'r') as f:
            cursor.execute('CREATE DATABASE {};'.format(dbname))
            cursor.execute(f.read())
        conn.commit()
    return


def create_profile():
    pass

def insert_paper():
    pass
