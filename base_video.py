import sqlite3 as sq
import os


def write_video(file_path, downloaded_file):
    """Функция добавляет видеофайл в папку со всеми видео"""
    with open(f'{file_path}.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)
    return True


def read_db():
    global db_file
    with sq.connect(db_file + '.db') as con:
        cur = con.cursor()
        cur.execute("""SELECT * FROM base_vid""")
        rows = cur.fetchall()
        return rows


def get_less(id):
    global db_file
    with sq.connect(db_file + '.db') as con:
        cur = con.cursor()
        if id == 0:
            res = read_db()
            return (res)
        else:
            table = read_db()
            table_id = [i[0] for i in table]
            id = table_id.index(id)
            return table[id][1:]


def set_less(n_id, n_name, n_link):
    f = get_less(0)
    ids = [i[0] for i in f]
    if n_link[-4:] == '.mp4' and n_id not in ids:
        global db_file
        with sq.connect(db_file + '.db') as con:
            cur = con.cursor()
            cur.execute(
                f"""INSERT INTO base_vid (ID, NAME, LINK) VALUES(?, ?, ?)""", (n_id, n_name, n_link))


def del_less(id):
    global db_file
    with sq.connect(db_file + '.db') as con:
        link = get_less(id=id)[-1]
        os.remove(path=link)
        cur = con.cursor()
        cur.execute(f"""DELETE FROM {name_table} WHERE ID={id}""")
    return True


def edit_less(id, name, link):
    with sq.connect(db_file + '.db') as con:
        cur = con.cursor()
        cur.execute(
            f"UPDATE {name_table} SET NAME = '{name}' WHERE ID = {id}")


def create_base():
    global db_file
    with sq.connect(db_file + '.db') as con:
        cur = con.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {name_table} (
				ID INTEGER PRIMARY KEY,
				NAME TEXT,
				LINK TEXT)""")


def remove_db():
    global db_file
    with sq.connect(db_file + '.db') as con:
        cur = con.cursor()
        cur.execute(f"DROP TABLE {name_table}")


db_file = "base_videos_test"
name_table = 'base_vid'
