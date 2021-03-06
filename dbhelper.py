import sqlite3


class DBHelper:

    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS items (description text, owner text)")
        self.conn.commit()

    def add_item(self, item_text, owner):
        self.conn.execute(
            "INSERT INTO items (description, owner) VALUES (?, ?)",
            (item_text, owner))
        self.conn.commit()

    def delete_item(self, item_text, owner):
        self.conn.execute(
            "DELETE FROM items WHERE description = (?) AND owner = (?)",
            (item_text, owner))
        self.conn.commit()

    def get_items(self, owner):
        return [x[0] for x in self.conn.execute(
                "SELECT description FROM items WHERE owner=(?)", (owner, ))]
