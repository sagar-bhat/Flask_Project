'''
Imlementation of Flask Server
for storing and manipulating user
data in sqlite3 Database.

'''

import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, jsonify

app = Flask(__name__)
app.config.from_object(__name__)

'''
Load default config and override
config from an environment variable.

'''
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, "falcon.db"),
    SECRET_KEY="development key"
))
app.config.from_envvar("FLASKR_SETTINGS", silent=True)
app.url_map.strict_slashes = False


def connect_db():
    '''
    Connects to the specific database.

    '''

    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    '''
    Opens a new database connection if there
    is none yet for the current application
    context.

    '''

    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):

    '''
    Closes the database again at
    the end of the request.

    '''

    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


def init_db():
    '''
    Initializes the database
    as per schema.sql

    '''

    db = get_db()
    with app.open_resource("schema.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    '''
    Initializes the database.

    '''

    init_db()
    print "Initialized the database."


@app.route("/register", methods=["POST"])
def register_user():
    '''
    Registers a new user in the database
    by accepting all the user details.

    '''

    user_data = request.get_json()
    db = get_db()
    db.execute("insert into users(fname, lname, uname, pword, email, phone)" +
               "values (?, ?, ?, ?, ?, ?)",
               [user_data["fname"], user_data["lname"], user_data["uname"],
                user_data["pword"], user_data["email"], user_data["phone"]])
    db.commit()
    response = jsonify({"Response": "User Inserted Successfully!"})
    return response


@app.route("/users", methods=["GET"])
def get_users():
    '''
    Displays all the users already
    registered in the Database.

    '''
    user_data = request.get_json()
    db = get_db()
    cur = db.execute("select * from users")

    rows = cur.fetchall()
    user_entries = [dict(id=row[0], fname=row[1], lname=row[2],
                         uname=row[3], pword=row[4], email=row[5],
                         phone=row[6]) for row in rows]
    return jsonify(user_entries)


@app.route("/getuser/<id>", methods=["GET"])
def get_user(id):

    '''
    Searches the user in the database
    based on the entered User Id and returns
    the user details if the user exits.

    '''
    db = get_db()
    cur = db.execute("select * from users where id=?", id)

    row = cur.fetchone()

    if row is not None:
        user = [dict(uid=row[0], fname=row[1], lname=row[2],
                     uname=row[3], pword=row[4], email=row[5],
                     phone=row[6])]
    else:
        user = []
    return jsonify(user)


@app.route("/update", methods=["PUT"])
def update_user():
    '''
    Updates details of an existing
    user in the Database.

    '''

    user_data = request.get_json()
    db = get_db()
    db.execute("update users set fname=?, lname=?, uname=?," +
               " pword=?, email=?, phone=? where id=?",
               [user_data["fname"], user_data["lname"],
                user_data["uname"], user_data["pword"],
                user_data["email"], user_data["phone"],
                user_data["id"]])
    db.commit()
    response = jsonify({"Response": "User Record Updated Successfully!"})
    return response


@app.route("/delete", methods=["DELETE"])
def delete_user():
    '''
    Deletes an Existing
    User from the database

    '''

    user_data = request.get_json()
    db = get_db()
    db.execute("delete from users where id=?", [user_data["id"]])
    db.commit()
    response = jsonify({"Response": "User deleted Successfully!"})
    return response


if __name__ == '__main__':
    '''
    Runs the Server

    '''

    app.run()

