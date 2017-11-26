#!/usr/bin/python3
# mind@large raspi audio component
# 11/24/17
# updated: 11/25/17

import ampli
import receive
import boombox


def initialize_amp():
    amp = ampli.Ampli(volume=40)


if __name__ == '__main__':
    initialize_amp()
