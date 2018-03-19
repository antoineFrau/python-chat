# Python server chat Talki Walki

Chat will give the token to speak client by client. Client can only spoke if he got the token.

### Getting started

Class ChatServer have an object ChatProtocol whitch is the protocol of the server.
Class ChatClient have an object ClientConnection whitch contain all methodes to connect to server, receive, send data from server.
When you run ChatClient that will ask you to enter a nickname.
Then if you are the only client connected you'll need to wait until an other client connect to the server.
You can add many clients to the server and then you'll be able to speak turn by turn with them.

Have fun :-)

### Prerequisites

You need to use python2.7 to run the chat.

### How to

Run 
```
python2.7 Chatserver.py
```
then open 3 differents terminal.
Then run in each of them :
```
python2.7 ChatClient.py
```

## Authors

* **Antoine FRAU** - *Initial work* - [antoineFrau](https://github.com/antoineFrau)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
