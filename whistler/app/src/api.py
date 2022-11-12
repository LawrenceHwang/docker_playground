import logging
import random

import flask
import mysql.connector

logging.basicConfig(level=logging.WARNING)


class DBManager:
    def __init__(self, database="example", host="db", user="root", password_file=None):
        pf = open(password_file, "r")
        pf_password = pf.read()
        self.connection = mysql.connector.connect(
            user=user,
            password=pf_password,
            host=host,
            database=database,
            auth_plugin="mysql_native_password",
        )
        pf.close()
        self.cursor = self.connection.cursor()

    def populate_db(self):
        self.cursor.execute("DROP TABLE IF EXISTS fate")
        self.cursor.execute(
            "CREATE TABLE fate (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))"
        )

        self.cursor.executemany(
            "INSERT INTO fate (id, title) VALUES (%s, %s);",
            [(i, "Fate #%d" % i) for i in range(1, 5)],
        )
        self.connection.commit()

    def query_titles(self):
        self.cursor.execute("SELECT title FROM fate")
        rec = []
        for c in self.cursor:
            rec.append(c[0])
        return rec


server = flask.Flask(__name__)
conn = None


@server.route("/fate")
def getFate():
    global conn
    if not conn:
        conn = DBManager(password_file="/run/secrets/db-password")
        conn.populate_db()
    rec = conn.query_titles()

    result = []
    for c in rec:
        result.append(c)

    return flask.jsonify({"response": result})


@server.route("/saber")
def saber():
    q = [
        "As you can see, I am your Saber class servant.",
        "I'd like some more, too.",
        "Are you my Master?",
        "Understood, Master.",
    ]
    random.shuffle(q)

    return flask.jsonify({"response": q[0]})


@server.route("/")
def hello():
    return flask.jsonify({"response": "Hello this is fate!"})
