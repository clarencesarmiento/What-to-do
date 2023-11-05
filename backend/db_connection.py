import sqlite3


def connect_to_database():
    conn = None
    try:
        conn = sqlite3.connect('backend/AppDatabase.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS accounts "
                       "(fullname TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL);")
        cursor.close()

    except sqlite3.Error as e:
        print(f'SQLite Connection Error: {e}')

    finally:
        return conn


if __name__ == '__main__':
    connection = connect_to_database()
    connection.close()
