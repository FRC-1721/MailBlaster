# -*- coding: utf-8 -*-

# Tidal Force Robotics

import os
import sys
import logging

from .main import EmailBlaster

__author__ = 'FRC Team 1721'
__email__ = 'concordroboticsteam@gmail.com'
__version__ = os.environ.get('VERSION')


# Setup logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

bot = EmailBlaster()

logging.info(bot.get_hello_world())
logging.info(f"using version {__version__}")
