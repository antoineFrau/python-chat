"""
Classe basique du tchat server.
"""

import socket
import select
import json
import ChatProtocole


class ChatServer:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)

    inputs = inputs_address = outputs = []

    readable = writable = exceptional = []

    message_queues = ""

    chat_protocol = {}

    already_send = False

    user_disconnect = False

    def __init__(self, port=3492):
        self.server.bind(('', port))
        print("Serveur ON -> localhost:"+str(port))
        self.server.listen(10)
        self.inputs = [self.server]
        self.inputs_address = [self.server.getsockname()]
        self.chat_protocol = ChatProtocole.ChatProtocole()

    def close_server(self):
        for sock in self.chat_protocol.clients_connections:
            sock.close()

    def alreay_send_set(self, bool):
        self.already_send = bool

    def remove_from_inputs(self, server_adresse):
        for i in range(1, len(self.inputs_address)):
            if self.inputs_address[i] == server_adresse:
                del self.inputs[i]
                del self.inputs_address[i]
                return i

    def tuplify(self, listything):
        if isinstance(listything, list): return tuple(map(self.tuplify, listything))
        if isinstance(listything, dict): return {k: self.tuplify(v) for k, v in listything.items()}
        return listything

    def select(self):
        try:
            self.readable, self.writable, self.exceptional = select.select(self.inputs, self.chat_protocol.clients_connections, self.inputs)
        except socket.error:
            print()

    def start_listen(self):
        while self.inputs:
            self.select()
            for s in self.readable:
                if s is self.server:
                    connection, client_address = s.accept()
                    print('Nouvelle connection depuis : '+str(client_address))
                    connection.setblocking(0)
                    self.chat_protocol.add_client(connection)
                    self.inputs.append(connection)
                    self.inputs_address.append(client_address)
                else:
                    if s not in self.inputs:
                        pass
                    try:
                        data = s.recv(4096).decode()
                    except socket.error:
                        print("err")
                    if data:
                        data_jsonify = json.loads(data)
                        action = data_jsonify["action"]
                        content = data_jsonify["content"]
                        pseudo = data_jsonify["from"]
                        if action == "user_disconnect":
                            content[0] = content[0].encode('ascii', 'backslashreplace')
                            content = self.tuplify(content)
                            index = self.remove_from_inputs(content)
                            data_to_send = json.dumps({"action": "user_disconnect", "content": "Deconnection de "+pseudo, "from": pseudo})
                            if index-1 == self.chat_protocol.client_number:
                                self.already_send = False
                                self.user_disconnect = True
                            self.chat_protocol.send_to_all(data_to_send)
                        elif s.getpeername() == self.chat_protocol.get_client_speak_connection().getpeername():
                            data_to_send = json.dumps({"action": "message", "content": content, "from": pseudo})
                            self.chat_protocol.send_to_all(data_to_send)
                            self.already_send = False
                            self.chat_protocol.next_client()
                        if s not in self.outputs:
                            self.outputs.append(s)
            if self.user_disconnect:
                self.user_disconnect = False
                pass

            # Handle outputs
            for s in self.writable:
                if self.chat_protocol.get_client_speak_connection() is None or s is None:
                    break

                """ 
                ICI :
                self.chat_protocol.get_client_speak_connection().getpeername() 
                ne fonctionne pas quand un client par alors que cest a lui de parler .... incomprehensible 
                """
                try:
                    if not self.chat_protocol.waiting and not self.already_send and (
                            s.getpeername() == self.chat_protocol.get_client_speak_connection().getpeername()):
                        data_to_send = json.dumps({"action": "yourTurn", "content": "Cest a votre tour de parler"})
                        s.send(data_to_send)
                        self.already_send = True
                except socket.error:
                    self.chat_protocol.next_client()
                    print("haha")


#Lancement du server
c = ChatServer()
c.start_listen()