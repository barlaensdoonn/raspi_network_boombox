#!/usr/bin/python3
# mind@large raspi audio component
# 11/24/17
# updated: 12/1/17

import yaml
import logging
import logging.config
import socketserver


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
            return {'track': msg[0], 'volume': float(msg[1])}
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
            self.server.logger.info('asking boombox to play "{}" at volume {}'.format(msg['track'], msg['volume']))
            self.server.bmbx.play(msg['track'], msg['volume'])
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
            return {'track': msg[0], 'volume': float(msg[1])}
        except IndexError:
            return None

    def handle(self):
        self.server.logger.debug('client {} connected'.format(self.client_address[0]))
        msg = self.parse_msg()

        if msg and msg['track'] in self.server.bmbx.sounds.keys():
            self.server.logger.info('asking boombox to play "{}" at volume {}'.format(msg['track'], msg['volume']))
            self.server.bmbx.play(msg['track'], msg['volume'])
        else:
            self.server.logger.warning("invalid command '{}' received, ignoring...".format(self.decoded))

    def finish(self):
        '''finish method is always called by the base handler after handle method has completed'''

        self.server.logger.debug('closed connection from {}'.format(self.client_address[0]))


class ReceiveAndPlay(object):

    def __init__(self, bmbx):
        self.bmbx = bmbx
        self._initialize_logger()
        self._initialize_server()

    def _initialize_logger(self):
        with open('log.yaml', 'r') as log_conf:
            log_config = yaml.safe_load(log_conf)

        logging.config.dictConfig(log_config)
        self.logger = logging.getLogger('receive')
        self.logger.info('receive logger instantiated')

    def _initialize_server(self):
        hostport = ('', 9999)  # '' stands for all available interfaces
        self.logger.info('initializing open server on port {}'.format(hostport[1]))

        self.server = socketserver.TCPServer(hostport, TCPHandler)
        self.server.logger = self.logger
        self.server.bmbx = self.bmbx
