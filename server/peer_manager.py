
class PeerManager:
    def __init__(self):
        self.peers = {}  # holds both ways
        # map (ip_addr, port) to username
        # map username to (ip_addr, port)

    def connect(self, username: str, peer_addr: tuple) -> None:
        print(f"[accepting connection from peer:{peer_addr}]")
        self.peers[peer_addr] = username
        self.peers[username] = peer_addr
        print(f"[peer connected] || online [{len(self.peers)}]")

    def get_peer_list(self) -> list[str]:
        return [x for x in self.peers.values() if type(x) == type('')]

    def get_broadcast_list(self, sender_addr: tuple) -> list:
        res = []
        for x in self.peers.keys():
            if x == sender_addr or len(x) != 2: continue  # make sure its not a username
            res.append(x)
        return res

    def get_addr_username(self, peer_addr: tuple[str, int]) -> str:
        return self.peers[peer_addr]

    def get_username_addr(self, username: str) -> tuple[str, int]:
        return self.peers.get(username, None)


# class Peer:
#     def __init__(self, addr):
#         self.addr = addr