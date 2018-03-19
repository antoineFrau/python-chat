"""
Pas de utf-8 donc les commentaires seront vraiment moche
Objet qui serra assigne au client pour se connecter au server et effectuer differentes taches
"""
import socket
import string
import random


class ClientConnection:

    server_address = ()

    id_client = ''

    def __init__(self, address='localhost', port=3492):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (address, port)
        self.id_client = ClientConnection.gen_id()

    def connect(self):
        self.sock.connect(self.server_address)
        print(self.sock.getpeername())

    def send(self, message):
        self.sock.send(message)

    def receive(self, callback, number=1024):
        message = self.sock.recv(number).decode()
        return callback(message)

    def close(self):
        self.sock.close()

    def get_id_client(self):
        return self.id_client

    @staticmethod
    def gen_id(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))