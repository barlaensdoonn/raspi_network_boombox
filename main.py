#!/usr/bin/python3
# mind@large raspi audio component
# 11/24/17
# updated: 11/26/17

import yaml
import logging
import logging.config
from Adafruit_MAX9744 import MAX9744
from receive import ReceiveAndPlay
from boombox import Boombox


def initialize_logger():
    with open('log.yaml', 'r') as log_conf:
        log_config = yaml.safe_load(log_conf)

    logging.config.dictConfig(log_config)
    logger = logging.getLogger('main')
    logger.info('* * * * * * * * * * * * * * * * * * * *')
    logger.info('main logger instantiated')

    return logger


def initialize_amp(volume):
    amp = MAX9744()

    try:
        amp.set_volume(volume)
        logger.info('amp initialized @ volume {}'.format(volume))
    except OSError:
        logger.error('OSError encountered when trying to set amp volume, likely not using Adafruit MAX9744 amp')
        amp = None

    return amp


def initialize_boombox():
    boom = Boombox()
    logger.info('boombox initialized')

    return boom


def initialize_receive(bmbx):
    rcv = ReceiveAndPlay(bmbx)
    logger.info('receive initialized')

    return rcv


if __name__ == '__main__':
    logger = initialize_logger()
    amp = initialize_amp(40)
    bmbx = initialize_boombox()
    receive = initialize_receive(bmbx)

    try:
        logger.info('receive server entering serve_forever() loop')
        receive.server.serve_forever()
    except KeyboardInterrupt:
        receive.server.shutdown()
        receive.server.close()
        logger.info('...user exit received, shutting down server...')
