import mysql.connector
import json
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello,Mr. Docker!'

@app.route('/frc')
def get_frc():
    return 'Hello,Radi Frc!'

@app.route('/widgets')
def get_widgets():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="inventory"
    )
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM widgets;")

    row_headers = [x[0] for x in cursor.description]  # this will extract row headers

    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))

    cursor.close()

    return json.dumps(json_data)


@app.route('/addinventory')
def add_invent():
    mydb = mysql.connector.connect(
        host='mysqldb',
        user="root",
        password="p@ssw0rd1",
        database="inventory"
    )
    cursor = mydb.cursor()

    cursor.execute("INSERT INTO inventory.widgets (name, description) VALUES ('Franko', 'Radi u Crozu2.');")
    mydb.commit()
    cursor.close()

    return 'added to inventory'

@app.route('/initdb')
def db_init():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="mysql"
    )
    cursor = mydb.cursor()
    cursor.execute("DROP DATABASE IF EXISTS inventory;")
    cursor.execute("CREATE DATABASE inventory;")
    cursor.execute("USE inventory;")
    cursor.execute("DROP TABLE IF EXISTS widgets;")
    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255));")
    cursor.close()

    return 'init database'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
