import sqlite3

class Data:
    def __init__(self):
        super(Data, self).__init__()
        global db
        global cursor
        db = sqlite3.connect('pyqt5/budget_tracker/tracker.db')
        cursor = db.cursor()
        db.execute("PRAGMA foreign_keys = ON")

        self.create_connection()
        self.create_categories_table()
        self.create_transactions_table()

    def create_connection(self):
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Email TEXT,
            Username TEXT,
            Password TEXT)""")

    def add_new_user(self, email, username, password):
        cursor.execute("INSERT INTO users (Email, Username, Password) VALUES(?,?,?)", (email, username, password))
        db.commit()
    
    def get_user(self, email, password):
        cursor.execute("SELECT * FROM users WHERE email=? and password=?", (email, password))
        user = cursor.fetchone()
        db.commit()

        return user

    def get_user_id(self, email, password):
        cursor.execute("SELECT Id, Username FROM users WHERE email=? and password=?", (email, password))
        user_info = cursor.fetchone()
        db.commit()

        return list(user_info)

    def create_transactions_table(self):
        cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Type TEXT,
            Sum INTEGER,
            Comment TEXT,
            Date TEXT,
            User_id INTEGER,
            Category_tittle TEXT,
            FOREIGN KEY(User_id) REFERENCES users(Id),
            FOREIGN KEY(Category_tittle) REFERENCES categories(Tittle))""")

    def create_categories_table(self):
        cursor.execute("""CREATE TABLE IF NOT EXISTS categories (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Tittle TEXT,
            Type TEXT,
            User_id INTEGER,
            FOREIGN KEY(User_id) REFERENCES users(Id))""")
    
    def add_new_category(self, category, c_type, user_id):
        cursor.execute("INSERT INTO categories (Tittle, Type, User_id) VALUES(?,?,?)", (category, c_type, user_id))
        db.commit()

    def get_all_expence_categories(self, user_id):
        cursor.execute("SELECT Tittle FROM categories WHERE Type='Expence' and User_id=?", (user_id))
        all_expence_categories = cursor.fetchall()
        db.commit()

        return all_expence_categories

    def get_all_income_categories(self, user_id):
        cursor.execute("SELECT Tittle FROM categories WHERE Type='Income' and User_id=?", (user_id))
        all_expence_categories = cursor.fetchall()
        db.commit()

        return all_expence_categories


