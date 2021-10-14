import pytest
import os.path

from random import choice
from string import ascii_lowercase

from email_blaster.main import EmailBlaster
from email_blaster.keyValueTable import KeyValueTable
from email_blaster.cogs.check_email import split_into_chunks


@pytest.fixture
def app():
    return EmailBlaster()


@pytest.fixture
def kvt():
    return KeyValueTable('/tmp/test_table.db')


class TestApplication(object):

    def test_versioning(self, app):
        # App version must be present
        assert len(app.version) > 1

    def test_config_mountpoint(self, app):
        # Mountpoint must point where we expect
        assert os.path.isdir('/config') is True

    def test_key_value_table(self, kvt):
        kvt['bot_token'] = '0101u72636462615517'
        kvt['email_listen'] = 'doooooooooooooot'
        kvt['email_password'] = 'password'

        assert len(kvt.items()) == 3

        assert kvt['bot_token'] == '0101u72636462615517'

        kvt.close()

    def test_chunk_splitter(self):
        """
        Written by joe
        Tests if the chunksplitter makes
        Valid discord frames
        """

        test_message = "".join(choice(ascii_lowercase) for i in range(3500))

        split_message = split_into_chunks(test_message, 2000)

        for split in split_message:
            assert len(split) <= 2000
