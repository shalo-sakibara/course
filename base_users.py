import sqlite3


def create_base(name):
    con = sqlite3.connect(f'{name}.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        tg_id INTEGER PRIMARY KEY,
        tg_name TEXT
        )""")
    con.close()
    pass


def set_users(tg_id_user=None, tg_name_user=None):
    # Добавляет пользователя в базу данных, если он оплатил курс
    if tg_id_user != None and tg_name_user != None:
        with sqlite3.connect('users_0_junior.db') as con:
            cur = con.cursor()
            cur.execute(
                'INSERT INTO users (tg_id, tg_name) VALUES (?, ?)', (tg_id_user, tg_name_user))
            pass


def get_users(tg_id_user, tg_name_user):
    # Проверяет на наличие пользователя, среди оплативших (На случай, если человек очистил историюю чата)
    if tg_id_user != None and tg_name_user != None:
        with sqlite3.connect('users_0_junior.db') as con:
            cur = con.cursor()
            cur.execute("""SELECT * FROM users""")
            if (tg_id_user, tg_name_user) in cur:
                return True
            else:
                return False


def delit(user_id, user_name):
    with sqlite3.connect('users_0_junior.db') as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM users WHERE tg_id={user_id}")
