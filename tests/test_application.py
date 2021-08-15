import pytest

from email_blaster.main import EmailBlaster


@pytest.fixture
def app():
    return EmailBlaster()


class TestApplication(object):

    def test_return_value(self, app):
        assert app.get_hello_world() == "Hello, World"
