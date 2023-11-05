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
            cursor.execute('INSERT INTO accounts VALUES (?, ?, ?);',
                           (credential.fullname, credential.email, credential.password))
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
            password = str(account[2])
            if password != credentials.password:
                raise WrongPassword
            else:
                return account

    except conn.Error as e:
        print(f'SQLite Account Sign In Error: {e}')

    finally:
        del conn
