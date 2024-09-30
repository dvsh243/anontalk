import socket
import threading

class RendezvousServer:

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 55555))

        self.peers = []

        print("--- [rendezvous server initialized] ---")
        self.listen()
    
    def listen(self):
        """listens for all data recieved by rendezvous server and re-routes it accordingly"""
        while True:
            peer_data, peer_addr = self.sock.recvfrom(128)
            if peer_data.decode() == 'connect': 
                self.connect(peer_addr)
            else:  # its a command
                self.recv_command(peer_data, peer_addr)

    def connect(self, peer_addr: tuple) -> None:
        print(f"[accepting connection from peer:{peer_addr}]")
        self.sock.sendto(b'ready', peer_addr)

        self.peers.append(peer_addr)

        print(f"[peer connected]")
        print(f"online: {self.peers}")


    def recv_command(self, command: str, peer_addr: tuple) -> None:
            """
            commands 
                -> '/connect' : direct connection to another peer
                -> '/online' : get all peer addresses currently connected
            """
            print(f"{peer_addr}> {command.decode()}")
            self.sock.sendto(b"testing response", peer_addr)



server = RendezvousServer()