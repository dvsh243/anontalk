import threading
from whisper import send_whisper

class Listener:
    def __init__(self, sock, peer):
        self.sock = sock
        self.peer = peer

    def start(self):
        listener_thread = threading.Thread(target=self.listen, daemon=True)
        listener_thread.start()

    def listen(self):
        while True:
            sender_data, sender_addr = self.sock.recvfrom(2048)
            sender_data = sender_data.decode()

            if sender_data.startswith("[WHISPER]"):
                send_whisper(self.sock, sender_data)
            else:
                print(f"\r{sender_data} \n> ", end='')