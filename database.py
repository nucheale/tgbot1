import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def print_users_db(self):
        self.cursor.execute('SELECT * FROM users')
        users = self.cursor.fetchall()
        return users

    def user_exists(self, bot_user_id):
        result = self.cursor.execute(f"SELECT * FROM users WHERE bot_id = '{bot_user_id}'").fetchone()
        if result is None:
            return False
        else:
            return True
    
    def add_user(self, username, bot_user_id):
        with self.connection:
            self.cursor.execute(f"INSERT INTO users (name, bot_id) SELECT '{username}', '{bot_user_id}' WHERE NOT EXISTS (SELECT 1 FROM users WHERE bot_id = '{bot_user_id}')")
            self.cursor.execute(f"UPDATE users SET status = 1 WHERE bot_id = '{bot_user_id}'")
            return
        
    def currency_included(self, bot_user_id, currency):
        result = self.cursor.execute(f"SELECT * FROM users_data WHERE bot_id = '{bot_user_id}' AND currency_name = '{currency}'").fetchall()
        if result == []:
            return False
        else:
            return True
    
    def add_currency(self, username, bot_user_id, currency):
        with self.connection:
            self.cursor.execute(f"INSERT INTO users_data (name, bot_id, currency_name) VALUES ('{username}', '{bot_user_id}', '{currency}')")
            return
        
    def remove_currency(self, bot_user_id, currency):
        with self.connection:
            self.cursor.execute(f"DELETE FROM users_data WHERE bot_id = '{bot_user_id}' AND currency_name = '{currency}'")
            return
        
    def list(self, bot_user_id):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM users_data WHERE bot_id = '{bot_user_id}'")
            currency_list = self.cursor.fetchall()
            return currency_list
        
    def list_all(self):
        self.cursor.execute(f"SELECT DISTINCT currency_name FROM currencies")
        currency_list = self.cursor.fetchall()
        return currency_list
    
    def remove_all(self, bot_user_id):
        with self.connection:
            self.cursor.execute(f"DELETE FROM users_data WHERE bot_id = '{bot_user_id}'")
            currency_list = self.cursor.fetchall()
            return currency_list
        
    def add_top(self, username, bot_user_id, currency):
        with self.connection:
            self.cursor.execute(f"INSERT INTO users_data (name, bot_id, currency_name) SELECT '{username}', '{bot_user_id}', '{currency}' WHERE NOT EXISTS (SELECT 1 FROM users_data WHERE bot_id = '{bot_user_id}' AND currency_name = '{currency}')")
            return
        
    def select_time(self, bot_user_id):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM users WHERE bot_id = '{bot_user_id}'")
            user_time = self.cursor.fetchall()[0][4]
            return user_time
     
    def set_time(self, time, bot_user_id):
        with self.connection:
            self.cursor.execute(f"UPDATE users SET time = '{time}' WHERE bot_id = '{bot_user_id}'")
            return
    # def get_currencies_now(self)

    def add_currency_price(self, currency_name, currency_price):
        with self.connection:
            self.cursor.execute(f"INSERT INTO currencies (currency_name, currency_price, timestamp) VALUES ('{currency_name}', {currency_price}, '{datetime.now()}')")
            return