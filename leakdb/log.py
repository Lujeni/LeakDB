# -*- coding: utf-8 -*-

from logging import getLogger, INFO, Formatter
from logging.handlers import RotatingFileHandler

logger = getLogger()
logger.setLevel(INFO)
formatter = Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

file_handler = RotatingFileHandler('/tmp/leakdb.log', 'a', 1000000, 1)
file_handler.setLevel(INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
