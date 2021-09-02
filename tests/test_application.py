import pytest
import os.path

from email_blaster.main import EmailBlaster


@pytest.fixture
def app():
    return EmailBlaster()


class TestApplication(object):

    def test_versioning(self, app):
        # App version must be present
        assert len(app.version) > 1

    def test_config_readable(self, app):
        # Config must have these sections
        assert app.config.sections() == ['discord', 'mail']

    def test_config_mountpoint(self, app):
        # Mountpoint must point where we expect
        assert os.path.isdir('/config') is True
