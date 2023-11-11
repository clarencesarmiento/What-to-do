import string
from email_validator import validate_email, EmailNotValidError
from secrets import token_hex
import re
import hashlib

from backend.app_backend import get_salt


class AccountRegistration:
    def __init__(self):
        self._fullname = None
        self._email = None
        self._password = None

    @property
    def fullname(self) -> str:
        return self._fullname

    @fullname.setter
    def fullname(self, fullname: str):
        if fullname is None or fullname == '':
            raise ValueError('Fullname field is Required.')
        elif not re.match(r'^[A-Za-z]+(?: [A-Za-z]+)*$', fullname):
            raise ValueError('Fullname has invalid character.')

        self._fullname = fullname

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str):
        if email is None or email == '':
            raise ValueError('Email field is Required.')
        try:
            email_info = validate_email(email, check_deliverability=True)
            email = email_info.normalized
        except EmailNotValidError:
            raise ValueError('Email is invalid.')

        self._email = email

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str):
        # Define criteria for password strength
        length_criteria = 8

        # Check the password entry
        if password is None or password == '':
            raise ValueError('Password field is Required.')
        # Check the length of the password
        elif len(password) < length_criteria:
            raise ValueError(f'Password should be at least {length_criteria} character long.')
        # Check for at least one uppercase letter
        elif not any(char.isupper() for char in password):
            raise ValueError('Password should contain at least one uppercase letter.')
        # Check for at least one lowercase letter
        elif not any(char.lower() for char in password):
            raise ValueError('Password should contain at least one lowercase letter.')
        # Check for at least one digit
        elif not any(char.isdigit() for char in password):
            raise ValueError('Password should contain at least one digit.')
        # Check for at least one special character
        elif not any(char in string.punctuation for char in password):
            raise ValueError('Password should contain at least one special character.')

        # Generate random salt
        salt = token_hex(16)

        # Combine the salt and the password
        salted_password = salt.encode() + password.encode()

        # Hash the salted password
        hashed_password = hashlib.sha256(salted_password).hexdigest()

        self._password = salt + '$' + hashed_password


class AccountSignIn:
    def __init__(self):
        self._email = None
        self._password = None

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str):
        if email is None or email == '':
            raise ValueError('Email field is Required.')
        try:
            email_info = validate_email(email, check_deliverability=True)
            email = email_info.normalized
        except EmailNotValidError:
            raise ValueError('Email is invalid.')

        self._email = email

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str):
        # Define criteria for password strength
        length_criteria = 8

        # Check the password entry
        if password is None or password == '':
            raise ValueError('Password field is Required.')
        # Check the length of the password
        elif len(password) < length_criteria:
            raise ValueError(f'Password should be at least {length_criteria} character long.')
        # Check for at least one uppercase letter
        elif not any(char.isupper() for char in password):
            raise ValueError('Password should contain at least one uppercase letter.')
        # Check for at least one lowercase letter
        elif not any(char.lower() for char in password):
            raise ValueError('Password should contain at least one lowercase letter.')
        # Check for at least one digit
        elif not any(char.isdigit() for char in password):
            raise ValueError('Password should contain at least one digit.')
        # Check for at least one special character
        elif not any(char in string.punctuation for char in password):
            raise ValueError('Password should contain at least one special character.')

        # Fetch Stored Salt
        stored_salt = get_salt(self.email)
        if stored_salt is not None:
            # Combine the sotred salt and password
            salted_password = stored_salt.encode() + password.encode()
            # Hash the salted password
            hashed_password = hashlib.sha256(salted_password).hexdigest()

            self._password = stored_salt + '$' + hashed_password


class ChangePassword:
    def __init__(self):
        self._email = None
        self._old_password = None
        self._new_password = None

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str):
        if email is None or email == '':
            raise ValueError('Email field is Required.')
        try:
            email_info = validate_email(email, check_deliverability=True)
            email = email_info.normalized
        except EmailNotValidError:
            raise ValueError('Email is invalid.')

        self._email = email

    @property
    def old_password(self) -> str:
        return self._old_password

    @old_password.setter
    def old_password(self, old_password: str):
        # Define criteria for password strength
        length_criteria = 8

        # Check the password entry
        if old_password is None or old_password == '':
            raise ValueError('Password field is Required.')
        # Check the length of the password
        elif len(old_password) < length_criteria:
            raise ValueError(f'Password should be at least {length_criteria} character long.')
        # Check for at least one uppercase letter
        elif not any(char.isupper() for char in old_password):
            raise ValueError('Password should contain at least one uppercase letter.')
        # Check for at least one lowercase letter
        elif not any(char.lower() for char in old_password):
            raise ValueError('Password should contain at least one lowercase letter.')
        # Check for at least one digit
        elif not any(char.isdigit() for char in old_password):
            raise ValueError('Password should contain at least one digit.')
        # Check for at least one special character
        elif not any(char in string.punctuation for char in old_password):
            raise ValueError('Password should contain at least one special character.')

        # Fetch Stored Salt
        stored_salt = get_salt(self.email)
        if stored_salt is not None:
            # Combine the sotred salt and password
            salted_password = stored_salt.encode() + old_password.encode()
            # Hash the salted password
            hashed_password = hashlib.sha256(salted_password).hexdigest()

            self._old_password = stored_salt + '$' + hashed_password

    @property
    def new_password(self) -> str:
        return self._new_password

    @new_password.setter
    def new_password(self, new_password: str):
        # Define criteria for password strength
        length_criteria = 8

        # Check the password entry
        if new_password is None or new_password == '':
            raise ValueError('Password field is Required.')
        # Check the length of the password
        elif len(new_password) < length_criteria:
            raise ValueError(f'Password should be at least {length_criteria} character long.')
        # Check for at least one uppercase letter
        elif not any(char.isupper() for char in new_password):
            raise ValueError('Password should contain at least one uppercase letter.')
        # Check for at least one lowercase letter
        elif not any(char.lower() for char in new_password):
            raise ValueError('Password should contain at least one lowercase letter.')
        # Check for at least one digit
        elif not any(char.isdigit() for char in new_password):
            raise ValueError('Password should contain at least one digit.')
        # Check for at least one special character
        elif not any(char in string.punctuation for char in new_password):
            raise ValueError('Password should contain at least one special character.')

        # Generate random salt
        salt = token_hex(16)

        # Combine the salt and the password
        salted_password = salt.encode() + new_password.encode()

        # Hash the salted password
        hashed_password = hashlib.sha256(salted_password).hexdigest()

        self._new_password = salt + '$' + hashed_password


class TaskCreation:
    def __init__(self):
        self._task = None

    @property
    def task(self) -> str:
        return self._task

    @task.setter
    def task(self, task):
        if task is None or task == '':
            raise ValueError

        self._task = task
