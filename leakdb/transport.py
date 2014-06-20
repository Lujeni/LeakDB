# -*- coding: utf-8 -*-

from zmq import Context, PUB, SUB, SUBSCRIBE

import leakdb
from leakdb.exceptions import UnknownStorageException


class ZeroLeakServer(object):

    def __init__(self, bind_addr, storage_type, **storage_kwargs):
        """
        :param str bind_addr: Bind the socket to an address.
        :param str storage_type: The storage type.
        :param dict storage_kwargs: list of parameters to instanciate the storage.
        """

        self.bind_addr = bind_addr
        self.storage_type = storage_type
        self.storage_kwargs = storage_kwargs

    def _init_socket(self):
        self.context = Context()
        self.socket = self.context.socket(SUB)
        self.socket.setsockopt(SUBSCRIBE, "zeroleak")
        self.socket.bind("tcp://{}".format(self.bind_addr))

    def run(self):
        """
        """
        storage = getattr(leakdb, self.storage_type, None)
        if not storage:
            raise UnknownStorageException(self.storage_type)
        self.storage = storage(**self.storage_kwargs)

        self._init_socket()
        while True:
            json_msg = self.socket.recv_json()
            pass


class ZeroLeakClient(object):

    def __init__(self, connect_address):
        self.connect_address = connect_address

    def __init_socket(self):
        self.context = Context()
        self.socket = self.context.socket(PUB)
        self.socket.connect("tcp://{}".format(self.connect_address))
