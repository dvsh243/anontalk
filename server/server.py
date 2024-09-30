import socket
import threading

class RendezvousServer:

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 55555))

        self.peers = []

        print("--- [rendezvous server initialized] ---")
    
    def listen(self):
        """listens for all data recieved by rendezvous server and re-routes it accordingly"""
        while True:
            peer_data, peer_addr = self.sock.recvfrom(128)
            if peer_data.decode() == 'connect':   # add with something because then any of the client can send 'connect' and server will consider it a connection request
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
            command = command.decode()
            print(f"{peer_addr}> {command}")

            # implement a dynamic pipeline where i can add commands and functions for them dynamically

            if command == '/online':
                # remove self from the list, since cant connect to self
                self.sock.sendto(f"ONLINE[{len(self.peers)}]: {self.peers}".encode(), peer_addr)
            
            elif command.startswith('/connect'):
                pass

            else:
                self.sock.sendto(b"invalid command", peer_addr)
                 



server = RendezvousServer()
# implement cronjob that pings all peers and check for availability
server.listen()  # non blocking