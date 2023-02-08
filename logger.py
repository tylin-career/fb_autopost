import logging
from datetime import datetime


class Logger:
    def __init__(self, applicationName):
        format = '%(asctime)s %(levelname)-8s %(message)s'
        # format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        logging.basicConfig(format=format)
        self.logger = logging.getLogger(applicationName)
        self.logger.setLevel(logging.INFO)
        self.logger.info("UTC: %s" % (datetime.utcnow()))
        self.logger.info("Local server time: %s", datetime.now())

    def get_logger(self):
        return self.logger
