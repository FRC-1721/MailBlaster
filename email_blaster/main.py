# Tidal Force robotics
# 2021, Email Blaster
# MIT License


import os
import sys
import logging

# Setup logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class EmailBlaster(object):

    def __init__(self):
        self.version = os.environ.get('GIT_COMMIT')

    def run(self):
        logging.info(f"using version {self.version}")
