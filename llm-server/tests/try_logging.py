import logging

logging.basicConfig(level=logging.DEBUG,
                    filename="logfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.debug('innocent debug message')
logger.info('useless piece of information')
logger.warning('Im warning you! ')
logger.error('Its an error, idiot')
logger.critical('You should go and touch grass')