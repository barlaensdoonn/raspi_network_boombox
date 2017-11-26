#!/usr/bin/python3
# mind@large raspi audio component
# 11/24/17
# updated: 11/25/17

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
        self.mixer = mixer
        self.mixer.init(frequency=44100)
        self.sounds = {key: self.mixer.Sound(self.tracks[key]) for key in selftracks.keys()}

    def play(track):
        '''returns mixer.Channel object that sound is playing on'''
        logging.info('playing {}'.format(track))

        return self.sounds[track].play(loops=-1)

    def set_volume(channel, volume):
        '''volume should be between 0.0 - 1.0'''
        channel.set_volume(volume)

    def stop(channel, ms):
        '''fades out audio over input milliseconds and releases channel back to the mixer'''
        logging.info('stopping playback on channel {}'.format(channel))
        channel.fadeout(ms)

    def pause(channel):
        channel.pause()

    def unpause(channel):
        channel.unpause()
