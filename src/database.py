# archivo: db.py
import sqlite3


def create_connection():
    connection = sqlite3.connect('project_management.db')
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            clearance TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            info TEXT,
            state TEXT,
            due_date TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_responsibles (
            task_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY (task_id) REFERENCES tasks(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            comment TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    ''')

    connection.commit()
    connection.close()


def query(query_str):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(query_str)
    data = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return data


def insert_one(insert_str):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(insert_str)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    print({usuario['name']: usuario for usuario in query("select * from users")})