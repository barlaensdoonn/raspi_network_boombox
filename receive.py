#!/usr/bin/python3
# mind@large raspi audio component
# 11/24/17
# updated: 6/8/18

import os
import yaml
import socket
import logging
import logging.config
import socketserver


def get_basepath():
    '''
    getting the script's basepath is needed when running the script
    as a systemd service on the Pi
    '''
    return os.path.dirname(os.path.realpath(__file__))


def initialize_logger():
    config_path = os.path.join(get_basepath(), 'log.yaml')
    with open(config_path, 'r') as log_conf:
        log_config = yaml.safe_load(log_conf)

    logging.config.dictConfig(log_config)
    logger = logging.getLogger('main')
    logger.info('* * * * * * * * * * * * * * * * * * * *')
    logger.info('main logger instantiated')

    return logger


class UDPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the client.
    """

    def parse_msg(self):
        '''
        self.request consists of a pair of data and client socket, and since
        there is no connection the client address must be given explicitly
        when sending data back via sendto().
        '''

        data = self.request[0]
        self.decoded = data.decode().strip()
        self.server.logger.info("{} wrote: {}".format(self.client_address[0], self.decoded))

        msg = self.decoded.split('/')

        try:
            return {'host': msg[0], 'track': msg[1], 'volume': float(msg[2])}
        except IndexError:
            return None

    def reply(self):
        '''
        reply to the sender. since there is no connection in a UDP socket
        the client address must be given explicitly in sendto().
        '''

        socket = self.request[1]
        socket.sendto(self.decoded.upper().encode(), self.client_address)

    def handle(self):
        self.server.logger.debug('client {} connected'.format(self.client_address[0]))
        msg = self.parse_msg()

        if msg and msg['track'] in self.server.bmbx.sounds.keys():
            if msg['host'] == self.server.hostname:
                self.server.logger.info('asking boombox to play "{}" at volume {}'.format(msg['track'], msg['volume']))
                self.server.bmbx.play(msg['track'], msg['volume'])
            else:
                self.server.logger.info('received valid command {}, but not addressed to me, ignoring...'.format(self.decoded))
        else:
            self.server.logger.warning("invalid command '{}' received, ignoring...".format(self.decoded))

    def finish(self):
        '''finish method is always called by the base handler after handle method has completed'''

        self.server.logger.debug('closed connection from {}'.format(self.client_address[0]))


class TCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the client.
    """

    def parse_msg(self):
        '''self.request is the TCP socket connected to the client'''

        data = self.request.recv(1024)
        self.decoded = data.decode().strip()
        self.server.logger.info("{} wrote: {}".format(self.client_address[0], self.decoded))

        msg = self.decoded.split('/')

        try:
            return {'host': msg[0], 'track': msg[1], 'volume': float(msg[2])}
        except IndexError:
            return None

    def handle(self):
        self.server.logger.debug('client {} connected'.format(self.client_address[0]))
        msg = self.parse_msg()

        if msg and msg['track'] in self.server.bmbx.sounds.keys():
            if msg['host'] == self.server.hostname:
                self.server.logger.info('asking boombox to play "{}" at volume {}'.format(msg['track'], msg['volume']))
                self.server.bmbx.play(msg['track'], msg['volume'])
            else:
                self.server.logger.info('received valid command {}, but not addressed to me, ignoring...'.format(self.decoded))
        else:
            self.server.logger.warning("invalid command '{}' received, ignoring...".format(self.decoded))

    def finish(self):
        '''finish method is always called by the base handler after handle method has completed'''

        self.server.logger.debug('closed connection from {}'.format(self.client_address[0]))


class ReceiveAndPlay(object):

    def __init__(self, bmbx, socket_type='udp'):
        '''server defaults to UDP. set socket_type="tcp" to use TCP sockets'''

        self.logger = self._initialize_logger()
        self.bmbx = bmbx
        self.socket_type = socket_type.lower()
        self.server = self._initialize_server()

    def _initialize_logger(self):
        config_path = os.path.join(get_basepath(), 'log.yaml')
        with open(config_path, 'r') as log_conf:
            log_config = yaml.safe_load(log_conf)

        logging.config.dictConfig(log_config)
        logger = logging.getLogger('receive')
        logger.info('receive logger instantiated')

        return logger

    def _initialize_server(self):
        hostport = ('', 9999)  # '' stands for all available interfaces
        hostname = socket.gethostname()
        self.logger.info('host {hostname} initializing open {socket_type} server on port {port}'.format(hostname=hostname, socket_type=self.socket_type.upper(), port=hostport[1]))

        if self.socket_type == 'udp':
            server = socketserver.UDPServer(hostport, UDPHandler)
        elif self.socket_type == 'tcp':
            server = socketserver.TCPServer(hostport, TCPHandler)
        else:
            raise Exception("invalid socket type, server not initialized")
            return None

        server.logger = self.logger
        server.hostname = hostname
        server.bmbx = self.bmbx

        return server
