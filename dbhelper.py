import sqlite3


class DBHelper:

    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS items (description text)")
        self.conn.commit()

    def add_item(self, item_text):
        self.conn.execute(
            "INSERT INTO items (description) VALUES (?)", (item_text, ))
        self.conn.commit()

    def delete_item(self, item_text):
        self.conn.execute(
            "DELETE FROM items WHERE description = (?)", (item_text, ))
        self.conn.commit()
