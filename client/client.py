import socket
import threading
import sys


class Peer:

    def __init__(self, port: int) -> None:
        self.RENDEZVOUS = ('127.0.0.1', 55555)
        self.SENDER_ADDR = self.RENDEZVOUS  # by default on '> ', change when p2p

        self.PORT = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', self.PORT))
        
        self.connect_rendezvous()

        print(f"--- [peer initialized | port:{self.PORT}] ---")

        self.listen()
        self.send_command()

        
    def listen(self) -> None:
        listener = threading.Thread(target = self.listener_thread, daemon=True)
        listener.start()
        print(f"--- [listening thread started] ---")


    def listener_thread(self) -> None:
        while True:
            sender_data, sender_addr = self.sock.recvfrom(2048)
            sender_data = sender_data.decode()

            if sender_addr == self.RENDEZVOUS:

                if sender_data.startswith('updateSender'):
                    ip, port = sender_data.split(' ')[1:]
                    self.connect_init_p2p( (ip, int(port)) )
                    print(f"updated {self.SENDER_ADDR=}")
                    continue

                print(f"\rRENDEZVOUS> {sender_data}\n> ", end='')


            else:
                
                if sender_data == '/disconnect': # the peer decided to disconnect 
                    print(f"[{self.SENDER_ADDR} decided to disconnect]")                
                    self.SENDER_ADDR = self.RENDEZVOUS
                    continue

                print(f"{sender_addr}> {sender_data}\n> ", end='')


    def connect_rendezvous(self):
        print(f"--- [connecting to rendezvous] ---")

        self.sock.sendto(b'connect', self.RENDEZVOUS)

        data = self.sock.recv(1024)
        print(f"rendezvous: {data.decode()}")


    def send_command(self):
        while True:
            msg = input('> ')

            if msg.startswith('/') and self.SENDER_ADDR != self.RENDEZVOUS:
                self.sock.sendto(b'/disconnect', self.SENDER_ADDR) 
                self.SENDER_ADDR = self.RENDEZVOUS  # commands go to the rendezvous server
                print(f"[SENDER_ADDR set to Rendezvous]")

            self.sock.sendto(msg.encode(), self.SENDER_ADDR)


    def connect_init_p2p(self, peer_addr):
        print(f"[initializing connection with {peer_addr}]")
        self.SENDER_ADDR = peer_addr
    

peer = Peer( int(sys.argv[1]) )
