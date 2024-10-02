import socket
from peer_manager import PeerManager
from message_handler import MessageHandler


class RendezvousServer:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 55555))

        self.peer_manager = PeerManager()
        self.message_handler = MessageHandler(self.sock, self.peer_manager)
        
        print(f"--- [rendezvous server initializing] ---")

    def listen(self):
        while True:
            peer_data, peer_addr = self.sock.recvfrom(128)
            peer_data = peer_data.decode()

            self.message_handler.handle(peer_data, peer_addr)
            self.display_message(peer_addr, peer_data)
        
    def display_message(self, peer_addr: tuple[str, int], message: str):
        username = self.peer_manager.get_addr_username(peer_addr)
        print(f"{username}> {message}")



server = RendezvousServer()
server.listen() # blocking