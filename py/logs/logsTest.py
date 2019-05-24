# -*- coding: utf-8 -*-

'''loggingTest

    Learn logs of python.
'''


import logging


# basic log config
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s: %(message)s')

logging.debug('DEBUG info')
logging.info('INFO info')
logging.warning('WARN config file %s not found', 'server.conf')
logging.error('ERROR info')
logging.critical('CRITICAL info')



