import sqlite3

sql_create_db = """
    CREATE TABLE IF NOT EXISTS anime(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        year DATE,
        count_episodes INTEGER,
        genre_id INTEGER,
        FOREIGN KEY (genre_id) REFERENCES genre(id)
    );
    CREATE TABLE IF NOT EXISTS genre(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT
    );
"""
db_path = 'db/anime.db'

genre_default = [
    ("экшн",),
    ("ужасы",),
    ("романтика",)
]


def dict_factory(cursor, row):
    """
    Получаем данные в виде dict
    :param cursor:
    :param row:
    :return:
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_db():
    with sqlite3.connect(db_path) as conn:
        curs = conn.cursor()
        conn.executescript(sql_create_db)
        data = curs.execute('SELECT * FROM genre').fetchall()
        if len(data) == 0:
            conn.executemany('INSERT INTO genre (title) VALUES (?)', genre_default)
            print('inserted default')


def create_xlsx():
    from xlsxwriter.workbook import Workbook
    workbook = Workbook('anime.xlsx')
    worksheet = workbook.add_worksheet()

    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        data = c.execute("select * from anime")
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)

    workbook.close()


def get_all_genre():
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = dict_factory
        curs = conn.cursor()
        data = curs.execute('SELECT id, title FROM genre').fetchall()
        return data


def add_genre(title):
    with sqlite3.connect(db_path) as conn:
        conn.executescript(f"INSERT INTO genre (title) \
                                    VALUES ('{title}')")
        print('inserted genre')


def get_all_anime():
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = dict_factory
        curs = conn.cursor()
        data = curs.execute('SELECT *, (select title FROM genre WHERE id=genre_id) as genre_name FROM anime').fetchall()
        return data


def create_anime(**kwargs):
    title, year, count_episodes, genre = kwargs.values()

    with sqlite3.connect(db_path) as conn:
        conn.executescript(f"INSERT INTO anime (title, year, count_episodes, genre_id) \
                            VALUES ('{title}', {year}, {int(count_episodes)}, {genre})")
        print('inserted anime')
