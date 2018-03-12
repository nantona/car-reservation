import os
import datetime
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'car_reservation.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    rv = sqlite3.connect(
        app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    sqlite3.dbapi2.converters['DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/', methods=['GET'])
def show_entries():
    db = get_db()
    cur = db.execute(
        """
        SELECT car_code, name, car_prj_code, start_datetime, end_datetime
        FROM ((reservations INNER JOIN cars ON reservations.car_id = cars.car_id)
        INNER JOIN persons ON reservations.person_id = persons.person_id)
        INNER JOIN car_projects ON cars.car_prj_id = car_projects.car_prj_id;
        """
    )
    reservations = cur.fetchall()
    cur = db.execute('SELECT car_id, car_code FROM cars')
    cars = cur.fetchall()
    cur = db.execute('SELECT person_id, name FROM persons')
    persons = cur.fetchall()
    return render_template('show_entries.html', reservations=reservations, cars=cars, persons=persons)


@app.route('/', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute(
        """
        INSERT INTO reservation (car_id, person_id, start_datetime, end_datetime)
        VALUES (?, ?, ?, ?)
        """,
        [request.form['car_id'],
         request.form['person'],
         request.form["start_date"] + " " + request.form["start_time"] + ":00",
         request.form["end_date"] + " " + request.form["end_time"] + ":00"])
    db.commit()
    print(request.form["end_date"] + " " + request.form["end_time"])
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/car_admin', methods=['GET'])
def show_cars():
    db = get_db()
    cur = db.execute(
        """
        SELECT car_id, car_code, car_prj_code
        FROM cars
        INNER JOIN car_projects
        ON cars.car_prj_id = car_projects.car_prj_id
        """
    )
    cars = cur.fetchall()
    cur.execute('SELECT car_prj_id, car_prj_code FROM car_projects')
    car_projects = cur.fetchall()
    return render_template('car_admin.html', cars=cars, car_projects=car_projects)


@app.route('/car_admin', methods=['POST'])
def add_car():
    db = get_db()
    db.execute(
        """
        INSERT INTO cars (car_code, car_prj_id)
        VALUES (?, ?)
        """,
        [request.form['car_code'], request.form['car_prj_id']])
    db.commit()
    return redirect(url_for('show_cars'))


@app.route('/sys_admin', methods=['GET'])
def show_sys_info():
    db = get_db()
    cur = db.execute('SELECT car_prj_code FROM car_projects')
    car_projects = cur.fetchall()
    return render_template('sys_admin.html', car_projects=car_projects)


@app.route('/sys_admin', methods=['POST'])
def add_car_prj():
    db = get_db()
    db.execute(
        '''
        INSERT INTO car_projects (car_prj_code)
        VALUES (?)
        ''',
        [request.form['car_prj_code']])
    db.commit()
    return redirect(url_for('show_sys_info'))


if __name__ == '__main__':
    app.run(debug=True)
