import socket


class RendezvousClient:
    def __init__(self, sock, rendezvous_addr):
        self.sock = sock
        self.RENDEZVOUS_ADDR = rendezvous_addr

    def connect(self):
        self.sock.sendto(b'connect', self.RENDEZVOUS_ADDR)
        data = self.sock.recv(1024)
        print(f"rendezvous: {data.decode()}")