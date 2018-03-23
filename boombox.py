# raspi network boombox
# 11/24/17
# updated: 3/23/18

import os
import yaml
import logging
import logging.config
from pygame import mixer


class Boombox(object):
    '''audo files must be .ogg or .wav'''

    def __init__(self):
        self._initialize_logger()
        self.mixer = mixer
        self.mixer.init(frequency=44100)
        self.sound_path = 'sound/'
        self.playables = self._get_playables()
        self.sounds = {key[0:2]: self.mixer.Sound(self.playables[key]) for key in self.playables.keys()}

    def _initialize_logger(self):
        with open('log.yaml', 'r') as log_conf:
            log_config = yaml.safe_load(log_conf)

        logging.config.dictConfig(log_config)
        self.logger = logging.getLogger('boombox')
        self.logger.info('boombox logger instantiated')

    def _get_playables(self):
        playables = {}

        with os.scandir(self.sound_path) as sounds:
            for sound in sounds:
                if sound.name.endswith('.ogg') or sound.name.endswith('.wav'):
                    playables[sound.name] = sound.path

        return playables

    def _set_volume(self, sound, volume):
        '''volume should be between 0.0 - 1.0'''

        self.logger.info('setting volume of sound "{}" to {}'.format(sound, volume))
        self.sounds[sound].set_volume(volume)

    def _is_playing(self, sound_object):
        '''pygame method that returns # of channels sound is playing on'''

        return sound_object.get_num_channels()

    def play(self, sound, volume=1.0):
        '''set volume of the sound and play it if not playing already'''

        swnd = self.sounds[sound]
        self._set_volume(sound, volume)

        if not self._is_playing(swnd):
            self.logger.info('playing sound "{}"'.format(sound))
            swnd.play()

    def stop(self, sound, fadeout=1000):
        '''fades out sound over specified milliseconds'''

        self.logger.info('stopping playback of {}'.format(sound))
        self.sounds[sound].fadeout(fadeout)

    def pause(self, channel):
        self.logger.info('pausing playback on {}'.format(channel))
        channel.pause()

    def resume(self, channel):
        self.logger.info('resuming playback on {}'.format(channel))
        channel.unpause()
