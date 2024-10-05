import socket
import sys
from rendezvous_client import RendezvousClient
from listener import Listener
from sender import Sender


class Peer:

    def __init__(self, port: int) -> None:
        self.RENDEZVOUS = ('127.0.0.1', 55555)
        self.SENDER_ADDR = self.RENDEZVOUS

        self.PORT = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind( ('0.0.0.0', self.PORT) )

        self.rendezvous_client = RendezvousClient(self.sock, self.RENDEZVOUS)
        self.listener = Listener(self.sock, self)
        self.sender = Sender(self.sock, self)

        self.connect_rendezvous()
        self.start_listener()  # non blocking
        self.start_sender()  # blocking

    def connect_rendezvous(self):
        self.username = self.rendezvous_client.connect()

    def start_listener(self):
        self.listener.start()

    def start_sender(self):
        self.sender.start()


peer = Peer(int(sys.argv[1]))