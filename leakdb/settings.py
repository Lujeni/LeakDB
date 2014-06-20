# -*- coding: utf-8 -*-

import os


# TODO: useless file, use .ini
class BaseSettings(object):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DEBUG = True

    QUEUE_WAIT_EMPTY = 1
