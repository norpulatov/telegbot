import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_file="database.db"):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, sub_expire TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS invoices (user_id INTEGER, price INTEGER, period INTEGER)")
        self.conn.commit()

    def user_exists(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        return bool(self.cursor.fetchone())

    def add_user(self, user_id):
        expire = datetime.now() + timedelta(days=1)
        self.cursor.execute("INSERT INTO users (user_id, sub_expire) VALUES (?, ?)", (user_id, expire.isoformat()))
        self.conn.commit()

    def get_sub_expire(self, user_id):
        self.cursor.execute("SELECT sub_expire FROM users WHERE user_id=?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return datetime.fromisoformat(result[0])
        return None

    def set_invoice(self, user_id, price, period):
        self.cursor.execute("DELETE FROM invoices WHERE user_id=?", (user_id,))
        self.cursor.execute("INSERT INTO invoices (user_id, price, period) VALUES (?, ?, ?)", (user_id, price, period))
        self.conn.commit()

    def get_invoice(self, user_id):
        self.cursor.execute("SELECT price, period FROM invoices WHERE user_id=?", (user_id,))
        return self.cursor.fetchone()

    def activate_sub(self, user_id, period):
        expire = datetime.now() + timedelta(days=period)
        self.cursor.execute("UPDATE users SET sub_expire=? WHERE user_id=?", (expire.isoformat(), user_id))
        self.conn.commit()
