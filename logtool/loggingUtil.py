# -*- coding:utf-8 -*-
import logging
import logging.handlers
import datetime
def logUtil():
    logger = logging.getLogger('mylogger')
    #设置日志级别
    logger.setLevel(logging.DEBUG)
    today=datetime.date.today()
    #每个月写入新的文件
    formatted_today=today.strftime('%y%m')
    #日志目录
    logFilePath = '/usr/local/odoo/'
    debugPath = logFilePath + 'debug' + formatted_today + '.log'
    errorPath = logFilePath + 'error' + formatted_today + '.log'

    rf_handler = logging.handlers.TimedRotatingFileHandler(debugPath, when='midnight', interval=1, backupCount=7)
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[at line:%(lineno)d] - %(message)s"))
    #error日志的日志级别
    f_handler = logging.FileHandler(errorPath)
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[at line:%(lineno)d] - %(message)s"))
    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)
    return logger

if __name__ == '__main__':
    pass
    #logger.debug('debug message')
    #logger.info('info message')
    #logger.warning('warning message')
    #logger.error('error message')
    #logger.critical('critical message')
