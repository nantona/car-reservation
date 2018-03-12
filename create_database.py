import sqlite3
import datetime

conn = sqlite3.connect('car_reservation.db',
                       detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
sqlite3.dbapi2.converters['DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS reservations;")
cur.execute(
    """
    CREATE TABLE reservations (
    'reservation_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'car_id' INTEGER NOT NULL,
    'person_id' INTEGER NOT NULL,
    'start_datetime' DATETIME,
    'end_datetime' DATETIME
    );
    """
)
cur.executemany(
    """
    INSERT INTO reservations (car_id, person_id, start_datetime, end_datetime)
    VALUES (?, ?, ?, ?);
    """,
    [[1, 1, "2014-01-02 23:45:00", "2014-01-02 23:45:00"],
     [2, 2, "2014-01-02 23:45:00", "2014-01-02 23:45:00"],
     [3, 3, "2014-01-02 23:45:00", "2014-01-02 23:45:00"]])

cur.execute("DROP TABLE IF EXISTS cars;")
cur.execute(
    """
    CREATE TABLE cars (
        'car_id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'car_code' TEXT NOT NULL,
        'car_prj_id' INTEGER NOT NULL
    );
    """
)
cur.executemany(
    "INSERT INTO cars (car_code, car_prj_id) VALUES (?, ?);",
    [["A0851", 1], ["X4786", 2], ["D625A", 3]])

cur.execute("DROP TABLE IF EXISTS car_projects;")
cur.execute(
    """
    CREATE TABLE car_projects (
        'car_prj_id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'car_prj_code' TEXT NOT NULL
    );
    """
)
cur.executemany(
    "INSERT INTO car_projects (car_prj_code) VALUES (?);",
    [["F-15"], ["F-16"], ["A-10"]])

cur.execute("DROP TABLE IF EXISTS persons;")
cur.execute(
    """
    CREATE TABLE persons (
        'person_id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'name' TEXT NOT NULL
    );
    """
)
cur.executemany(
    "INSERT INTO persons (name) VALUES (?);",
    [["高田社長"], ["中本浩二"], ["アレックス"]])

conn.commit()
conn.close()
