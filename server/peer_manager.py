import socket


class PeerManager:
    def __init__(self):
        self.peers = {}  # map (ip_addr, port) to username

    def connect(self, username: str, peer_addr: tuple) -> None:
        print(f"[accepting connection from peer:{peer_addr}]")
        self.peers[peer_addr] = username
        print(f"[peer connected] || online [{len(self.peers)}]")

    def get_peer_list(self) -> list[str]:
        return list(self.peers.values())

    def get_broadcast_list(self, sender_addr: tuple) -> list:
        return [x for x in list(self.peers.keys()) if x != sender_addr]

    def get_addr_username(self, peer_addr: tuple[str, int]) -> str:
        return self.peers[peer_addr]


# class Peer:
#     def __init__(self, addr):
#         self.addr = addr