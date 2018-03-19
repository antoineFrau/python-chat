"""
Classe gestion Client.
"""

import ClientConnection
import json
import signal
import sys


class ChatClient:
    SIGINT = False

    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.client = ClientConnection.ClientConnection()
        self.client.connect()
        self.listen()
        signal.signal(signal.SIGINT, self.disconnect_event)

    def ask_for_message(self):
        message = raw_input("C'est a " + self.pseudo + " de parler : ")
        data_to_send = {"action": "message", "content": message, "from": self.pseudo}
        self.client.send(json.dumps(data_to_send))
        self.listen()

    def listen(self):
        self.client.receive(self.read_data, 4096)

    def disconnect_event(self, signal, frame):
        #Gestion du CTR+C
        data_to_send = {"action": "user_disconnect", "content": self.client.sock.getsockname(), "from": self.pseudo}
        self.client.send(json.dumps(data_to_send))
        self.client.close()
        sys.exit()

    def read_data(self, data):
        if data:
            try:
                jsonify = json.loads(data)
                action = jsonify["action"]
                content = jsonify["content"]
                # gestion des differentes actions possible.
                if action == "yourTurn":
                    self.ask_for_message()
                elif action == "message":
                    msg_from = jsonify["from"]
                    print(msg_from+": "+content)
                elif action == "welcome":
                    print(content)
                elif action == "wait":
                    print(content)
                elif action == "user_disconnect":
                    print(content)
            except ValueError:
                """
                Si l'utilisateur prend trop de temps pour ecrire son message des informations peuvent lui etre adresse donc quand il aura envoye son message
                toutes les informations au format json arriveront en meme temps donc on les decortique ici.  
                """
                for d in data.split('}'):
                    d += '}'
                    self.read_data(d)


cli = ChatClient(raw_input("Entrez votre pseudo : "))

while(1):
    cli.listen()
