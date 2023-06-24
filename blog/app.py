from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, content TEXT NOT NULL)')

@app.before_first_request
def before_first_request():
    init_db()

def close_db_connection(conn):
    conn.close()

if __name__ == '__main__':
    app.run()





