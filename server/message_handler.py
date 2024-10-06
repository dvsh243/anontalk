from peer_manager import PeerManager


class MessageHandler:
    def __init__(self, sock, peer_manager: PeerManager):
        self.peer_manager = peer_manager
        self.sock = sock

        self.commands = {
            '/connect': self.handle_connect,  # this is a system generated command, dont let a peer enter this command
            '/online': self.handle_online,    # get a list of all online usernames
            '/whisper': self.handle_whisper,  # privately message a peer (message goes through server)
            '/block': self.handle_block       # block the user and you wont see him on your feed
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

        _, username = message.split(' ')[:2]
        whisper_msg = "".join( message.split(' ')[2:] )
        whisper_addr = self.peer_manager.get_username_addr(username)

        if not whisper_addr:
            self.handle_invalid_command(peer_addr)
            return

        # print(f"[whispering] {whisper_addr} -- {whisper_msg}")
        self_user = self.peer_manager.get_username_addr(peer_addr)
        self.send_message(f"{self_user} whispered> {whisper_msg}", whisper_addr)
        
    
    def handle_block(self, message: str, peer_addr: tuple[str, int]):
        to_block_user = message.split(' ')[1]
        to_block_addr = self.peer_manager.get_username_addr(to_block_user)

        self.peer_manager.add_block(peer_addr, to_block_addr)


    def handle_invalid_command(self, peer_addr):
        self.send_message("invalid command", peer_addr)

    def send_message(self, message, peer_addr):
        self.sock.sendto(message.encode(), peer_addr)