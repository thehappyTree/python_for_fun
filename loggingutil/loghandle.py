# -*- coding:utf-8 -*-
import logging
class LoggingHandle:
    def __init__(self):
        pass


def test():
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)
    logging.log(logging.DEBUG,'this is debug log')
    logging.log(logging.INFO, "This is a info log.")
    logging.log(logging.WARNING, "This is a warning log.")
    logging.log(logging.ERROR, "This is a error log.")
    logging.log(logging.CRITICAL, "This is a critical log.")

if __name__ == '__main__':
    test()
