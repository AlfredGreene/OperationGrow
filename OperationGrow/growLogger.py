import time
import logging
import logging.handlers as handlers

filename = 'log'

logger = logging.getLogger('OperationGrow')
logger.setLevel(logging.INFO)
handler = logging.handlers.TimedRotatingFileHandler(filename=filename, when='d', interval=1, backupCount=14, encoding=None, delay=False, utc=False)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def info(msg):
    logger.info(msg)
