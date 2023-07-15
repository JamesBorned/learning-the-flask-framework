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