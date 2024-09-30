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

            if sender_addr == self.RENDEZVOUS:
                print(f"\rRENDEZVOUS> {sender_data.decode()}\n> ", end='')
            else:
                print(f"{sender_addr}> {sender_data.decode()}\n> ", end='')


    def connect_rendezvous(self):
        print(f"--- [connecting to rendezvous] ---")

        self.sock.sendto(b'connect', self.RENDEZVOUS)

        data = self.sock.recv(1024)
        print(f"rendezvous: {data.decode()}")


    def send_command(self):
        while True:
            msg = input('> ')
            self.sock.sendto(msg.encode(), self.SENDER_ADDR)


peer = Peer( int(sys.argv[1]) )
