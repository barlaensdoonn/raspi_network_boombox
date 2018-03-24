# raspi network boombox
# 11/24/17
# updated: 3/23/18

import os
import yaml
import logging
import logging.config
from pygame import mixer


class Boombox(object):
    '''audo files must be .ogg or .wav, all other types will be ignored'''

    sound_dir = 'sound/'

    def __init__(self, frequency=44100, channels=2):
        self._initialize_logger()
        self.mixer = self._initialize_mixer(frequency=frequency, channels=channels)
        self.sound_path = os.path.join(self._get_basepath(), self.sound_dir)
        self.tracks = self._get_tracks()
        self.sounds = {key[0:2]: self.mixer.Sound(self.tracks[key]) for key in self.tracks.keys()}

    def _get_basepath():
        '''
        this method of getting the script's basepath is needed
        when running the script as a systemd service on the Pi
        '''
        return os.path.dirname(os.path.realpath(__file__))

    def _initialize_logger(self):
        log_config = os.path.join(self._get_basepath(), 'log.yaml')

        with open(log_config, 'r') as log_conf:
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

    def _check_active_sounds(self):
        '''
        mixer.get_busy() returns 1 if any sounds are currently being mixed
        it will return 1 even if the sound is paused
        '''
        if not self.mixer.get_busy():
            self.logger.info('mixer has no active sound objects')
            return False
        else:
            return True

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
        '''pause all currently playing sounds. if none are playing, do nothing'''

        if self._check_active_sounds():
            self.logger.info('pausing all sounds')
            self.mixer.pause()

    def resume_all(self):
        '''resume all currently paused sounds. if none are paused, do nothing'''

        if self._check_active_sounds():
            self.logger.info('resuming all sounds')
            self.mixer.unpause()

    def stop_all(self, fadeout=1000):
        '''stop playback of all currently playing sounds. if none are playing, do nothing'''

        if self._check_active_sounds():
            self.logger.info('stopping playback of all sounds')
            self.mixer.fadeout(fadeout)
