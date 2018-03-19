"""
Classe qui permet de gerer le protocole du tchat.
1 user connecte : On lui dit de pateinter
2 users ils peuvent communiquer ect ect

Utilisation du json pour communiquer
"""

import json
import socket
import errno


class ChatProtocole():

    def __init__(self):
        self.clients_connections = []
        self.waiting = False
        self.client_number = 0

    def add_client(self, client_connection):
        self.clients_connections.append(client_connection)
        print(len(self.clients_connections))
        if len(self.clients_connections) == 1:
            data_to_send = json.dumps({"action": "wait", "content": "Welcome dude !\nEn attente d'un autre utilisateur."})
            client_connection.send(data_to_send)
            self.waiting = True
        else:
            data_to_send = json.dumps({"action": "welcome", "content": "Welcome dude !"})
            client_connection.send(data_to_send)
            self.waiting = False

    def get_client_speak_connection(self):
        if len(self.clients_connections) > 1:
            client_connection = self.clients_connections[self.client_number]
            return client_connection
        else:
            #err il faut mini 2 users
            pass

    def delete_user(self, peername):
        for sock in self.clients_connections:
            if peername == sock.getpeername():
                sock.close()
                if self.client_number == self.clients_connections.index(sock):
                    self.clients_connections.remove(sock)
                    self.next_client()
                    return
                self.clients_connections.remove(sock)
                return

    def next_client(self):
        if len(self.clients_connections) == 1:
            self.waiting = True
        if self.client_number >= len(self.clients_connections)-1:
            self.client_number = 0
        else:
            self.client_number += 1

    def send_to_all(self, message):
        for sock in self.clients_connections:
            try:
                sock.send(message)
                # Si il y a une erreur c'est que le socket s'est deconnecte
            except socket.error, e:
                if isinstance(e.args, tuple):
                    if e[0] == errno.EPIPE:
                        index = self.clients_connections.index(sock)
                        self.clients_connections.remove(sock)
                        if len(self.clients_connections) < self.client_number:
                            self.client_number = len(self.clients_connections)
                        if len(self.clients_connections) == 1:
                            self.waiting = True
                            data_to_send = json.dumps(
                                {"action": "wait", "content": "En attente d'un autre utilisateur."})
                            self.send_to_all(data_to_send)
                        if self.client_number == index:
                            self.next_client()
                break
