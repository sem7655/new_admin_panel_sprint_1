import os

from dotenv import load_dotenv

load_dotenv()

import sqlite3

from contextlib import closing

from datetime import datetime, date, time

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Film_work:
    title: str
    description: str
    type: str
    creation_date: datetime
    created: datetime
    modified: datetime
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Person:
    full_name: str
    created: datetime
    modified: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Genre:
    name: str
    description: str
    created: datetime
    modified: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Genre_film_work:
    created: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Person_film_work:
    created: datetime
    role: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)




psycopg2.extras.register_uuid()


def save_film_work_to_postgres(conn: psycopg2.extensions.connection, film_works):
    conn1 = conn.cursor()
    for film_work in film_works:
        conn1.execute(
            "INSERT INTO content.film_work (id, title, description, creation_date, rating, type, created, modified) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s ) ON CONFLICT DO NOTHING",
            (film_work.id, film_work.title, film_work.description, film_work.creation_date, film_work.rating,
             film_work.type,
             film_work.created, film_work.modified))


def save_person_to_postgres(conn: psycopg2.extensions.connection, persons):
    conn1 = conn.cursor()
    for person in persons:
        conn1.execute("INSERT INTO content.person (id, full_name, created, modified) "
                      "VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                      (person.id, person.full_name, person.created, person.modified))


def save_genre_to_postgres(conn: psycopg2.extensions.connection, genres):
    conn1 = conn.cursor()
    for genre in genres:
        conn1.execute("INSERT INTO content.genre (id, name, description, created, modified) "
                      "VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                      (genre.id, genre.name, genre.description, genre.created, genre.modified))


def save_genre_film_work_to_postgres(conn: psycopg2.extensions.connection, genre_film_works):
    conn1 = conn.cursor()
    for genre_film_work in genre_film_works:
        conn1.execute("INSERT INTO content.genre_film_work (id, film_work_id, genre_id, created) "
                      "VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                      (genre_film_work.id, genre_film_work.film_work_id, genre_film_work.genre_id,
                       genre_film_work.created))


def save_person_film_work_to_postgres(conn: psycopg2.extensions.connection, person_film_works):
    conn1 = conn.cursor()
    for person_film_work in person_film_works:
        conn1.execute("INSERT INTO content.person_film_work (id, film_work_id, person_id, role, created) "
                      "VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                      (person_film_work.id, person_film_work.film_work_id, person_film_work.person_id,
                       person_film_work.role, person_film_work.created))

#1
def load_movies_from_sqlite(connection: sqlite3.Connection, conn, n):
    movies_list = []

    cur = connection.cursor()
    cur.execute("select * from **film_work**")
    cur.row_factory = sqlite3.Row

    while True:
        rows = cur.fetchmany(n)
        if rows:
            for row in rows:
                movie = Film_work(
                    title=row["title"],
                    description=row["description"],
                    rating=rows["rating"],
                    type=rows["type"],
                    created=row["created"],
                    modified=row["modified"],
                    id=uuid.UUID(row["id"]),
                )
                movies_list.append(movie)

            save_film_work_to_postgres(conn, movies_list)
            movies_list = []
        else:
            break

#2
def load_genres_from_sqlite(connection: sqlite3.Connection, conn, n):
   genre_list = []
   cur = connection.cursor()
   cur.execute("select * from genre")
   cur.row_factory = sqlite3.Row

   while True:
       rows = cur.fetchmany(n)
       if rows:
           for row in rows:
               genre = Genre(
                   name=row["name"],
                   description=row["description"],
                   created=row["created"],
                   modified=row["modified"],
                   id=uuid.UUID(row["id"]),
               )
               genre_list.append(genre)
           save_genre_to_postgres(conn, genre_list)
           genre_list = []
       else:
           break


#3
def load_persons_from_sqlite(connection: sqlite3.Connection, conn, n):
   person_list = []
   cur = connection.cursor()
   cur.execute("select * from genre")
   cur.row_factory = sqlite3.Row

   while True:
       rows = cur.fetchmany(n)
       if rows:
           for row in rows:
               person = Person(
                   full_name=rows["full_name"],
                   created=row["created"],
                   modified=row["modified"],
                   id=uuid.UUID(row["id"]),
               )
               person_list.append(person)
           save_person_to_postgres(conn, person_list)
           person_list = []
       else:
           break

#4
def load_genre_film_work_from_sqlite(connection: sqlite3.Connection, conn, n):
   genre_film_work_list = []
   cur = connection.cursor()
   cur.execute("select * from genre")
   cur.row_factory = sqlite3.Row

   while True:
       rows = cur.fetchmany(n)
       if rows:
           for row in rows:
               genre_film_work = Genre_film_work(
                   film_work_id=uuid.UUID(row["id"]),
                   created=row["created"],
                   modified=row["modified"],
                   genre_id=uuid.UUID(row["id"]),
                   id=uuid.UUID(row["id"]),
               )
               genre_film_work_list.append(genre_film_work)
           save_genre_to_postgres(conn, genre_film_work_list)
           genre_film_work_list = []
       else:
           break

#5
def load_person_film_work_from_sqlite(connection: sqlite3.Connection, conn, n):
   person_film_work_list = []
   cur = connection.cursor()
   cur.execute("select * from genre")
   cur.row_factory = sqlite3.Row

   while True:
       rows = cur.fetchmany(n)
       if rows:
           for row in rows:
               person_film_work = Person_film_work(
                   film_work_id=uuid.UUID(row["id"]),
                   created=row["created"],
                   modified=row["modified"],
                   person_id=uuid.UUID(row["id"]),
                   id=uuid.UUID(row["id"]),
               )
               person_film_work_list.append(person_film_work)
           save_genre_to_postgres(conn, person_film_work_list)
           person_film_work_list = []
       else:
           break

def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    n = 5
    load_movies_from_sqlite(connection, pg_conn, n)
    load_genres_from_sqlite(connection, pg_conn, n)
    load_persons_from_sqlite(connection, pg_conn, n)
    load_genre_film_work_from_sqlite(connection, pg_conn, n)
    load_person_film_work_from_sqlite(connection, pg_conn, n)
    pg_conn.commit()


if __name__ == '__main__':
    dsl = {'dbname': os.environ.get('DB_NAME'), 'user': os.environ.get('DB_USER'),
           'password': os.environ.get('DB_PASSWORD'), 'host': os.environ.get('DB_HOST', '127.0.0.1'),
           'port': os.environ.get('DB_PORT', 5432)}
    with closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
        with sqlite3.connect('db.sqlite') as sqlite_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
        sqlite_conn.close()
