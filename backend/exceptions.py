class ApplicationError(Exception):
    """ Base Application exception that all others inherit.

    This is done to not pollute the built-in exceptions, which *could* result in
    unintended errors being unexpectedly and incorrectly handled within implemeters code.
    """


class AccountError(ApplicationError):
    """
        Account Related Errors.
    """


class AccountExistsError(AccountError):
    """ The Email already has an account. """

    def __init__(self, email: str):
        """
        :param str email:
            User's email address.
        """
        self.email = email
        super().__init__(self.error_string)

    @property
    def error_string(self):
        return f'{self.email} already has an account.'


class EmailNotFound(AccountError):
    """ The Email doesn't exist. """

    def __init__(self, email: str):
        """
        :param str email:
            User's email address.
        """
        self.email = email
        super().__init__(self.error_string)

    @property
    def error_string(self):
        return f"{self.email} doesn't exist."


class WrongPassword(AccountError):
    """ Entered a Wrong password. """

    def __init__(self, ):
        super().__init__(self.error_string)

    @property
    def error_string(self):
        return 'You have entered a Wrong Password.'
