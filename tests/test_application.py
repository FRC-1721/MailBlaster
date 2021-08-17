import pytest

from email_blaster.main import EmailBlaster


@pytest.fixture
def app():
    return EmailBlaster()


class TestApplication(object):

    def test_versioning(self, app):
        assert len(app.version) > 1
