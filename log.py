import logging

def init():
    logging.basicConfig(filename='example.log', level=logging.DEBUG)

def debug(msg):
    logging.debug(msg)

def error(msg):
    logging.error(msg, exec_info=True)
