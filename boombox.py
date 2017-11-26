#!/usr/bin/python3
# mind@large raspi audio component
# 11/24/17
# updated: 11/25/17

import logging
import logging.config
from pygame import mixer


class Boombox(object):
    '''
    there are 3 ways to handle starting/stopping sound playback in this case:

    1. start playing all tracks in indefinite loops on initialization and
       use mixer.Sound.set_volume() or mixer.Channel.set_volume() to modulate volume
    2. start playback when trigger is received, modulate volume as above, then call
       mixer.Channel.fadeout(ms) to stop sound and release the Channel when finished
    3. start playback in an indefinite loop when first trigger is received, modulate
       volume as in #1, and call mixer.Channel methods pause() or unpause() to start/stop

    main difference is in #2 the track starts playing from the beginning the next time it is triggered,
    whereas #1 is always looping regardless of volume, and #3 maintains state of the track's position
    '''

    tracks = {
        'monteverdi': '/home/pi/sound/Lagrime_damante_monteverdi_waved_16bit_PCM.wav'
    }

    def __init__(self):
        self._initialize_logger()
        self.mixer = mixer
        self.mixer.init(frequency=44100)
        self.sounds = {key: self.mixer.Sound(self.tracks[key]) for key in self.tracks.keys()}
        self.logger.debug('pygame mixer and sounds dict initiated')

    def _initialize_logger(self):
        with open('log.yaml', 'r') as log_conf:
            log_config = yaml.safe_load(log_conf)

        logging.config.dictConfig(log_config)
        self.logger = logging.getLogger('boombox')
        self.logger.info('boombox logger instantiated')


    def play(self, track):
        '''returns mixer.Channel object that sound is playing on'''
        self.logger.info('playing {}'.format(track))

        return self.sounds[track].play(loops=-1)

    def set_volume(self, channel, volume):
        '''volume should be between 0.0 - 1.0'''
        self.logger.info('setting volume on {} to {}'.format(channel, volume))
        channel.set_volume(volume)

    def stop(self, channel, ms):
        '''fades out audio over input milliseconds and releases channel back to the mixer'''
        self.logger.info('stopping playback on {}'.format(channel))
        channel.fadeout(ms)

    def pause(self, channel):
        self.logger.info('pausing playback on {}'.format(channel))
        channel.pause()

    def unpause(channel):
        self.logger.info('resuming playback on {}'.format(channel))
        channel.unpause()
