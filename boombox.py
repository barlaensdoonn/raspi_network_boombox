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

    def __init__(self, frequency=44100, channels=2):
        self._initialize_logger()
        self.mixer = self._initialize_mixer(frequency=frequency, channels=channels)
        self.sound_path = 'sound/'
        self.tracks = self._get_tracks()
        self.sounds = {key[0:2]: self.mixer.Sound(self.tracks[key]) for key in self.tracks.keys()}

    def _initialize_logger(self):
        with open('log.yaml', 'r') as log_conf:
            log_config = yaml.safe_load(log_conf)

        logging.config.dictConfig(log_config)
        self.logger = logging.getLogger('boombox')
        self.logger.info('boombox logger instantiated')

    def _initialize_mixer(self, frequency=44100, channels=2):
        '''initialize pygame mixer. set channels=1 for mono'''

        mixer.init(frequency=frequency, channels=channels)
        return mixer

    def _get_tracks(self):
        '''
        scans Boombox.sound_path and returns a dict of all audio files that end with .ogg or .wav
        format of the dict is {'filename': 'path_to_file'}
        '''

        tracks = {}

        with os.scandir(self.sound_path) as sounds:
            for sound in sounds:
                if sound.name.endswith('.ogg') or sound.name.endswith('.wav'):
                    tracks[sound.name] = sound.path

        return tracks

    def _is_playing(self, sound_object):
        '''pygame method that returns # of channels sound is playing on'''

        return sound_object.get_num_channels()

    def _set_volume(self, sound, volume):
        '''volume should be between 0.0 - 1.0'''

        self.logger.info('setting volume of sound "{}" to {}'.format(sound, volume))
        self.sounds[sound].set_volume(volume)

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
        '''this method needs the channel object a sound is playing on rather than the sound object'''

        self.logger.info('pausing playback on {}'.format(channel))
        channel.pause()

    def resume(self, channel):
        '''this method needs the channel object a sound is playing on rather than the sound object'''

        self.logger.info('resuming playback on {}'.format(channel))
        channel.unpause()

    def pause_all(self):
        '''pause all currently playing sounds'''


        self.logger.info('pausing all sounds')
        self.mixer.pause()
