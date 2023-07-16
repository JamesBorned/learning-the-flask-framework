import sqlite3
import math
import time

class FDataBase:
    def __init__(self, db): # db - ссылка на связь с базой данных
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu''' # выборка всех записей из таблицы меню
        try:
            self.__cur.execute(sql) # sql-запрос
            res = self.__cur.fetchall() # читаем все записи
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    # добавить данные в таблицу posts
    def addPost(self, title, text):
        try:
            tm = math.floor(time.time()) # время добавления
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?", (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД "+str(e))
            return False

        return True