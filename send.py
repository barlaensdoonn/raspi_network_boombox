#!/usr/bin/python3
# simple test sending track and volume to receive.server over sockets
# 11/26/17
# updated: 11/26/17

import socket


def encode_msg(track, volume):
    return '{}/{}\r\n'.format(track, volume).encode()


def context_client(hostport, state):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(hostport)
        client.sendall(state)

    return state.decode().strip()


if __name__ == '__main__':
    hostport = ('192.168.1.112', 9999)
    track = 'monteverdi'
    volume = '1.0'

    msg = context_client(hostport, encode_msg(track, volume))
    print('sent: {}'.format(msg))
