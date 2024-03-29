import sqlite3
import os
from flask import Flask, render_template, request, g, flash
from FDataBase import FDataBase

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
    dbase = FDataBase(db) # экземпляр класса
    return render_template('index.html', menu = dbase.getMenu())

@app.route("/add_post", methods=["POST","GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category = 'error')
            else:
                flash('Статья добавлена успешно', category = 'success')
        else:
            flash('Ошибка добавления статьи', category = 'error')

    return render_template('add_post.html', menu=dbase.getMenu(), title="Добавление статьи")

if __name__ == "__main__":
    app.run(debug=True)

@app.teardown_appcontext # уничтожение контекста приложения
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()