import socket


class RendezvousClient:
    def __init__(self, sock, rendezvous_addr):
        self.sock = sock
        self.RENDEZVOUS_ADDR = rendezvous_addr

    def connect(self):
        username = input("please enter a username: ")  # should be one word without hyphens
        self.sock.sendto(f"connect as - {username}".encode(), self.RENDEZVOUS_ADDR)

        data = self.sock.recv(1024)
        print(f"rendezvous: {data.decode()}\n> ", end='')