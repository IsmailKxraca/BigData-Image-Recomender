import sqlite3


# connect database
def connect_test_database():
    conn = sqlite3.connect('test_pictures.db')
    return conn


# creates the table for the picture paths
def create_path_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS picture_paths
                      (id INTEGER PRIMARY KEY,
                       path TEXT,
                       FOREIGN KEY (id) REFERENCES test_pictures(id))''')


# adds a path with id to the picture paths table
def add_path(conn, id, path):
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO picture_paths (id, path) VALUES (?, ?)", (id, path))
    conn.commit()


# gets the path of the input Id
def get_path_from_id(conn, id_to_find):
    cursor = conn.cursor()
    cursor.execute(f"SELECT Path FROM picture_paths WHERE ID = ?", (id_to_find,))
    result = cursor.fetchone()

    if result:
        path = result[0]
        return path
    else:
        return None


# returns the total amount of datapoints of the picture paths table
def get_record_count(conn):
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM picture_paths")
    count = cursor.fetchone()[0]
    return count


# prints the picture paths table
def show_path(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM picture_paths")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


# deletes everything in picture paths
def reset_database(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM picture_paths")
    conn.commit()


# deletes all datapoints with null at path
def clean_none(conn):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM picture_paths WHERE path IS NULL")

    conn.commit()

# closes connection
def close_test_pictures_connection(conn):
    conn.close()
