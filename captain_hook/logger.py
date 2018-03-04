# -*- coding: utf-8 -*-
import logging


def setup_logger():
    formatter = logging.Formatter(
        '%(created)s - %(name)s - %(levelname)s - %(message)s')

    werkzeug_log = _setup_logger('werkzeug', logging.INFO)
    hookbot_log = _setup_logger('hookbot', logging.DEBUG)
    _setup_logger('watchdog', logging.INFO)

    file_handler = _setup_file_handler(formatter)
    stream_handler = _setup_stream_handler(formatter)

    werkzeug_log.addHandler(file_handler)
    werkzeug_log.addHandler(stream_handler)

    hookbot_log.addHandler(stream_handler)
    hookbot_log.addHandler(file_handler)

    return hookbot_log


def _setup_logger(logger_name, level):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    return logger


def _setup_file_handler(formatter):
    file_handler = logging.FileHandler('hookbot.log')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    return file_handler


def _setup_stream_handler(formatter):
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    return stream_handler
