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

#Tabelle für den Pfad der Bilder
def create_path_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS picture_paths
                      (id INTEGER PRIMARY KEY,
                       path TEXT,
                       FOREIGN KEY (id) REFERENCES test_pictures(id))''')

# Methode zum Einfügen eines Datensatzes
def add_test_picture(conn, id, histogram):
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO test_pictures (id, histogram) VALUES (?, ?)", (id, histogram))
    conn.commit()

def add_path(conn, id, path):
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO test_pictures (id, path) VALUES (?, ?)", (id, path))
    conn.commit()

# Methode zum Abrufen und Ausgeben aller Datensätze
def show_test_pictures(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_pictures")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def show_path(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pictures_path")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def reset_database(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM test_pictures")
    conn.commit()
    cursor.execute("DELETE FROM picture_paths")
    conn.commit()

# Methode zum Beenden der Datenbankverbindung
def close_test_pictures_connection(conn):
    conn.close()




conn = connect_test_database()

create_table(conn)
create_path_table(conn)

show_test_pictures(conn)

close_test_pictures_connection(conn)

