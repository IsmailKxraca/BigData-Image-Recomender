import unittest
import sqlite3
import os


class TestDatabaseMethods(unittest.TestCase):
    def setUp(self):
        # Verbindung zur Testdatenbank herstellen
        self.conn = sqlite3.connect('test_pictures.db')
        self.cursor = self.conn.cursor()

        # Tabelle erstellen
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS test_pictures
                              (id INTEGER PRIMARY KEY,
                               histogram TEXT)''')


if __name__ == '__main__':
    unittest.main()
