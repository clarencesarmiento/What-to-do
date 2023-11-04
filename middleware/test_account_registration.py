from middleware.account_registration import AccountRegistration
import pytest


def test_init():
    acc_registration = AccountRegistration()


def test_set_valid_values_with_setter():
    acc_registration = AccountRegistration()
    acc_registration.fullname = 'John Doe'
    acc_registration.email = 'johndoe@gmail.com'
    acc_registration.password = 'JohnDoe@112'

    assert acc_registration.fullname == 'John Doe'
    assert acc_registration.email == 'johndoe@gmail.com'
    assert acc_registration != 'JohnDoe@112'


def test_fullname():
    acc_registration = AccountRegistration()

    valid_test_input = ['John Doe', 'Jennifer Smith', 'Samantha Grace Davis']
    for name in valid_test_input:
        acc_registration.fullname = name
        assert acc_registration.fullname == name

    require_test_input = ['', None]
    with pytest.raises(ValueError) as e:
        for test in require_test_input:
            acc_registration.fullname = test
            assert str(e.value) == 'Fullname field is Required.'

    invalid_test_input = ['John Do3', 'Jennifer@Smith', 'Samantha!!Grace_Davis']
    with pytest.raises(ValueError) as e:
        for test in invalid_test_input:
            acc_registration.fullname = test
            assert str(e.value) == 'Fullname has invalid character.'


def test_email():
    acc_registration = AccountRegistration()

    valid_test_input = ['johndoe@gmail.com', 'Jennifer.Smith@yahoo.com', 'davis_samGrace@me.org']
    for email in valid_test_input:
        acc_registration.email = email
        assert acc_registration.email == email

    require_test_input = ['', None]
    with pytest.raises(ValueError) as e:
        for test in require_test_input:
            acc_registration.email = test
            assert str(e.value) == 'Email field is Required.'

    invalid_test_input = ['johndoe.gmail.com', 'Jennifer.Smith@yah.com', 'davis_samGrace@me.o']
    with pytest.raises(ValueError) as e:
        for test in invalid_test_input:
            acc_registration.email = test
            assert str(e.value) == 'Email is invalid.'


def test_password():
    acc_registration = AccountRegistration()

    valid_test_input = ['Johndoe@112', 'Jennifer.Smith_241', 'Samantha_grace@1422']
    for password in valid_test_input:
        acc_registration.password = password
        assert acc_registration.password != password

    require_test_input = ['', None]
    with pytest.raises(ValueError) as e:
        for test in require_test_input:
            acc_registration.password = test
            assert str(e.value) == 'Password field is Required.'

    with pytest.raises(ValueError) as e:
        acc_registration.password = 'John!12'
        assert str(e.value) == 'Password should be at least 8 character long.'

    with pytest.raises(ValueError) as e:
        acc_registration.password = 'john!122'
        assert str(e.value) == 'Password should contain at least one uppercase letter.'

    with pytest.raises(ValueError) as e:
        acc_registration.password = 'JOHND122'
        assert str(e.value) == 'Password should contain at least one lowercase letter.'

    with pytest.raises(ValueError) as e:
        acc_registration.password = 'JohnDoe!'
        assert str(e.value) == 'Password should contain at least one digit.'

    with pytest.raises(ValueError) as e:
        acc_registration.password = 'JohnDoe122'
        assert str(e.value) == 'Password should contain at least one special character.'
