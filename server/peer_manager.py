import collections


class PeerManager:
    def __init__(self):
        self.peers = {}  # holds both ways
        # map (ip_addr, port) to username
        # map username to (ip_addr, port)

        self.blocked = collections.defaultdict(set)

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
            if (
                x == sender_addr or     # cant broadcast to self
                type(x) == type('') or  # since we store both addresses and usernames in the same map
                sender_addr in self.blocked[x]  # reciever `x` hasnt blocked sender `sender_addr`
            ): continue
            res.append(x)
        return res

    def get_addr_username(self, peer_addr: tuple[str, int]) -> str:
        return self.peers[peer_addr]

    def get_username_addr(self, username: str) -> tuple[str, int]:
        return self.peers.get(username, None)
    
    def add_block(self, sender_addr: tuple, block_addr: tuple):
        self.blocked[sender_addr].add(block_addr)


# class Peer:
#     def __init__(self, addr):
#         self.addr = addr