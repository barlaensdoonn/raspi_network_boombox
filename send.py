#!/usr/bin/python3
# simple test sending track and volume to receive.server over sockets
# 11/26/17
# updated: 11/26/17

import socket


def encode_msg(track, volume):
    return '{}/{}\r\n'.format(track, volume).encode()


def context_tcp_client(hostport, msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(hostport)
        client.sendall(msg)

    return msg.decode().strip()


def context_udp_broadcast(msg):
    hostport = ('<broadcast>', 9999)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        return sock.sendto(msg, hostport)  # returns number of bytes sent


if __name__ == '__main__':
    hostport = ('swnd.local', 9999)
    track = 'monteverdi'
    volume = '1.0'

    msg = context_tcp_client(hostport, encode_msg(track, volume))
    print('sent: {}'.format(msg))
