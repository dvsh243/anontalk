import json

class Sender:
    def __init__(self, sock, peer):
        self.sock = sock
        self.peer = peer

    def start(self):
        while True:
            msg = input('\r> ')
            self.sock.sendto(msg.encode(), self.peer.SENDER_ADDR)