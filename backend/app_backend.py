from backend.db_connection import connect_to_database
from backend.exceptions import *


def register_account(credential):
    """
    To insert account credentials to the database for account registration.

    :param credential: Fullname, Email, Password
    :return:
    """

    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Check if the email address already exist
        cursor.execute('SELECT * FROM accounts WHERE email = ?;', (credential.email,))
        account_exist = cursor.fetchall()

        if account_exist:
            raise AccountExistsError(credential.email)
        else:
            cursor.execute('INSERT INTO accounts (fullname, email, password) VALUES (?, ?, ?);',
                           (credential.fullname, credential.email, credential.password))

            cursor.execute('SELECT user_id FROM accounts WHERE email = ?;', (credential.email,))
            user_id = cursor.fetchone()[0]

            cursor.execute(f"""CREATE TABLE IF NOT EXISTS usertasks_{user_id}
                            (task_name TEXT NOT NULL, status TEXT NOT NULL);""")
            conn.commit()

        cursor.close()
        conn.close()
    except conn.Error as e:
        print(f'SQLite Account Registration Error: {e}')
    finally:
        del conn


def get_name(email):
    """
    To fetch the name from the database based on email.

    :param email: User's Email Address
    :return name: User's name
    """

    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Get fullname with the specified email address
        cursor.execute('SELECT fullname FROM accounts WHERE email = ?;', (email,))
        name = cursor.fetchone()

        if name:
            return str(name[0]).split(' ')[0]
        else:
            return 'User'

    except conn.Error as e:
        print(f'SQLite Fetching User Name Error: {e}')

    finally:
        del conn


def get_salt(email):
    """
    Get salt from the password based on email.

    :param email: User's Email Address
    :return salt: Salt required for hashing
    """

    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Get password with the speficied email
        cursor.execute('SELECT password FROM accounts WHERE email = ?;', (email,))
        password = cursor.fetchone()

        if password:
            salt = str(password[0]).split('$')[0]
            return salt
        else:
            return None

    except conn.Error as e:
        print(f'SQLite Fetching Salt Error: {e}')
    finally:
        del conn


def signin_account(credentials):
    """
    To fetch User account for Sign In.

    :param credentials: Email, Password
    :return account: Fullname, Email, Password
    """

    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM accounts WHERE email = ?;', (credentials.email,))
        account = cursor.fetchone()

        cursor.close()
        conn.close()

        if account is None:
            raise EmailNotFound(credentials.email)

        else:
            password = str(account[-1])
            if password != credentials.password:
                raise WrongPassword
            else:
                return account

    except conn.Error as e:
        print(f'SQLite Account Sign In Error: {e}')

    finally:
        del conn


def change_password(credentials):
    """
        To fetch User account for Sign In.

        :param credentials: Email, Password
        :return account: Fullname, Email, Password
        """

    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM accounts WHERE email = ?;', (credentials.email,))
        account = cursor.fetchone()

        if account is None:
            raise EmailNotFound(credentials.email)

        else:
            password = str(account[-1])
            if password != credentials.old_password:
                raise WrongPassword
            else:
                cursor.execute('UPDATE accounts SET password = ? WHERE email = ? AND password = ?;',
                               (credentials.new_password, credentials.email, credentials.old_password))
                conn.commit()

    except conn.Error as e:
        print(f'SQLite Change Passsword Error: {e}')

    else:
        cursor.close()
        conn.close()

    finally:
        del conn


def get_all_task(table_name):
    """
        To get all available task.

    :param table_name: User's table name.
    :return result: User's all available task.
    """

    conn = None
    result = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name};')
        result = cursor.fetchall()
        conn.commit()

    except conn.Error as e:
        print(f'SQLite Fetch Task Error: {e}')

    else:
        cursor.close()
        conn.close()

    finally:
        del conn
        return result


def add_new_task(table_name, task, status='To Do'):
    """
        Function to add new task in the user's table.

    :param table_name: User's table name.
    :param task: User's new task.
    :param status: Default task status.
    :return:
    """

    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name} WHERE task_name = ?;', (task,))
        task_exist = cursor.fetchone()

        if task_exist is None:
            cursor.execute(f'INSERT INTO {table_name} VALUES (?, ?);', (task, status))
            conn.commit()
        else:
            pass

    except conn.Error as e:
        print(f'SQLite Add New Task Error: {e}')

    else:
        cursor.close()
        conn.close()

    finally:
        del conn


def delete_task(table_name, task):
    """
        Function to delete user task.

    :param table_name: User's table name.
    :param task: User's task to delete.
    :return:
    """

    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM {table_name} WHERE task_name = ?;', (task,))
        conn.commit()

    except conn.Error as e:
        print(f'SQLite Delete Task Error: {e}')

    else:
        cursor.close()
        conn.close()

    finally:
        del conn


def update_status(table_name, task, status):
    """
        Function to update task status.

    :param table_name: User's table name.
    :param task: User's task to update status.
    :param status: New status of the task.
    :return:
    """

    conn = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(f'UPDATE {table_name} SET status = ? WHERE task_name = ?;', (status, task))
        conn.commit()

    except conn.Error as e:
        print(f'SQLite Updating Task Status Error: {e}')

    else:
        cursor.close()
        conn.close()

    finally:
        del conn


def update_count(table_name):
    """
        Function to fetch the count of the To Do and Done task.

    :param table_name: User's table name.
    :return: To Do count and Done count
    """

    conn = None
    todo_count = None
    done_count = None
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE status = 'To Do';")
        todo_count = cursor.fetchone()

        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE status = 'Done';")
        done_count = cursor.fetchone()

    except conn.Error as e:
        print(f'SQLite Fetch Task Count Error: {e}')

    else:
        cursor.close()
        conn.close()

    finally:
        del conn
        return todo_count, done_count
