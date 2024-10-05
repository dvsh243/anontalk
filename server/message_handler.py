import socket


class MessageHandler:
    def __init__(self, sock, peer_manager):
        self.peer_manager = peer_manager
        self.sock = sock

        self.commands = {
            '/connect': self.handle_connect,  # this is a system generated command, dont let a peer enter this command
            '/online': self.handle_online,
            '/whisper': self.handle_whisper,
        }

    def handle(self, message, peer_addr):
        if message.startswith('/'):
            self.handle_command(message, peer_addr)
        else:
            self.handle_message(message, peer_addr)

    def handle_message(self, message, peer_addr):
        # broadcast this to all peers
        for recv_peer_addr in self.peer_manager.get_broadcast_list(peer_addr):
            username = self.peer_manager.get_addr_username(peer_addr)
            self.send_message(f"{username}> {message}", recv_peer_addr)

    def handle_command(self, message, peer_addr):
        command = message.split(' ')[0]

        if command in self.commands:
            self.commands[command]( message, peer_addr )
        
        else: 
            self.handle_invalid_command(peer_addr)


    # add these functions dynamically using `setattr`
    def handle_connect(self, message: str, peer_addr: tuple[str, str]):
        username = message.split(' ')[1]
        self.peer_manager.connect(username, peer_addr)
        self.send_message("ready", peer_addr)


    def handle_online(self, message: str, peer_addr: tuple[str, str]):
        peer_list = self.peer_manager.get_peer_list()
        self.send_message(f"ONLINE[{len(peer_list)}]: {peer_list}", peer_addr)


    def handle_whisper(self, message: str, peer_addr: tuple[str, str]):
        pass

    def handle_invalid_command(self, peer_addr):
        self.send_message("invalid command", peer_addr)

    def send_message(self, message, peer_addr):
        self.sock.sendto(message.encode(), peer_addr)