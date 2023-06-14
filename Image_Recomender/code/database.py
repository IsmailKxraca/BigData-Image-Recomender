import sqlite3


# Methode zum Verbinden zur Datenbank
def connect_test_database():
    conn = sqlite3.connect('test_pictures.db')
    return conn


# Methode zum Erstellen der Tabelle
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS test_pictures
                      (id INTEGER PRIMARY KEY,
                       histogram TEXT)''')


# Methode zum Einfügen eines Datensatzes
def add_test_picture(conn, id, histogram):
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO test_pictures (id, histogram) VALUES (?, ?)", (id, histogram))
    conn.commit()


# Methode zum Abrufen und Ausgeben aller Datensätze
def show_test_pictures(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT histogram FROM test_pictures")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


# Methode zum Beenden der Datenbankverbindung
def close_test_pictures_connection(conn):
    conn.close()


# einmalige Ausführung zum erstellen
conn = connect_test_database()
show_test_pictures(conn)
