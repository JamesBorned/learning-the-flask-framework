import sqlite3
import os
from flask import Flask, render_template, request, g

# конфигурация
DATABASE = '/tmp/flsite.db'
DEBUG = True # режим отладки
SECRET_KEY = 'irjfirjfrkoejigjieorr'

app = Flask(__name__)
app.config.from_object(__name__) # загрузка конфигурации

app.config.update(dict(DATABASE=os.path.join(app.root_path,'flsite.db')))

# connection with db
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# creating db without launching of server
def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f: # read, contains sql-scripts
        db.cursor().executescript(f.read()) # class cursor
    db.commit() # write changes in db
    db.close() # close connection

def get_db():
    '''соединение с бд, если оно ещё не установлено'''
    if not hasattr(g, 'link_db'): # в g - установление соединения с базой данных
        g.link_db = connect_db()
    return g.link_db

@app.route("/")
def index():
    db = get_db() # установление соединения с бд
    return render_template('index.html', menu = [])

@app.teardown_appcontext # уничтожение контекста приложения
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()

