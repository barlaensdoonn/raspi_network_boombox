#!/usr/bin/python3
# mind@large raspi audio component
# 11/24/17
# updated: 11/25/17

import yaml
import receive
import boombox
import logging
import logging.config
from Adafruit_MAX9744 import MAX9744


def initialize_logger():
    with open('log.yaml', 'r') as log_conf:
        log_config = yaml.safe_load(log_conf)

    logging.config.dictConfig(log_config)
    logger = logging.getLogger('boombox')
    logger.info('* * * * * * * * * * * * * * * * * * * *')
    logger.info('boombox logger instantiated')

    return logger


def initialize_amp(volume):
    amp = MAX9744()
    amp.set_volume(volume)
    logger.info('amp initialized @ volume {}'.format(volume))

    return amp

def initialize_boombox():
    boom = boombox.Boombox()
    logger.info('boombox initialized')

    return boom


if __name__ == '__main__':
    logger = initialize_logger()
    amp = initialize_amp(40)
    bmbx = initialize_boombox()

    monti = bmbx.play('monteverdi')
    listen = True

    try:
        while listen:
            pass
    except KeyboardInterrupt:
        bmbx.stop(monti, 1000)
