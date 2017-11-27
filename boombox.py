#!/usr/bin/python3
# mind@large raspi audio component
# 11/24/17
# updated: 11/26/17

import yaml
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
        self.sounds = {key: self.mixer.Sound(self.tracks[key]) for key in self.tracks.keys()}  # dict to hold mixer.Sounds in same format as tracks dict
        self.logger.debug('pygame mixer and sounds dict initiated')

    def _initialize_logger(self):
        with open('log.yaml', 'r') as log_conf:
            log_config = yaml.safe_load(log_conf)

        logging.config.dictConfig(log_config)
        self.logger = logging.getLogger('boombox')
        self.logger.info('boombox logger instantiated')

    def _set_volume(self, sound, volume):
        '''volume should be between 0.0 - 1.0'''

        self.logger.info('setting volume of sound "{}" to {}'.format(sound, volume))
        self.sounds[sound].set_volume(volume)

    def _is_playing(self, sound_object):
        '''pygame method that returns # of channels sound is playing on'''

        return sound_object.get_num_channels()

    def play(self, sound, volume):
        '''set volume of the sound and play it if not playing already'''

        swnd = self.sounds[sound]
        self._set_volume(sound, volume)

        if not self._is_playing(swnd):
            self.logger.info('playing sound "{}"'.format(sound))
            swnd.play(loops=-1)

    def stop(self, sound):
        '''fades out sound over specified milliseconds'''

        self.logger.info('stopping playback of {}'.format(sound))
        self.sounds[sound].fadeout(1000)

    def pause(self, channel):
        self.logger.info('pausing playback on {}'.format(channel))
        channel.pause()

    def unpause(channel):
        self.logger.info('resuming playback on {}'.format(channel))
        channel.unpause()
