import logging
from Utilities import Constants

# config logger
FORMATE = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename='../AppLogs.log',
                    level=logging.DEBUG,
                    format=FORMATE,)

logger = logging.getLogger()


def getLogger():
    return logger
