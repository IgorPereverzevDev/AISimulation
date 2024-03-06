import os

import psycopg2
import logging
from contextlib import contextmanager

database_url = os.getenv('DATABASE_URL')


@contextmanager
def fetch_all(query, params=None):
    try:
        with psycopg2.connect(database_url) as conn, conn.cursor() as cursor:
            cursor.execute(query, params or [])
            rows = cursor.fetchall()
            yield rows
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        raise


@contextmanager
def fetch_one(query, params=None):
    try:
        with psycopg2.connect(database_url) as conn, conn.cursor() as cursor:
            cursor.execute(query, params or [])
            id = cursor.fetchone()
            yield id
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        raise


def insert_update_one(query, params=None):
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or [])
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Database operation failed: {error}")
        raise
