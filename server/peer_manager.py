import socket


class PeerManager:
    def __init__(self):
        self.peers = {}  # map username to (ip_addr, port)

    def connect(self, username: str, peer_addr: tuple) -> None:
        print(f"[accepting connection from peer:{peer_addr}]")
        self.peers[peer_addr] = username
        print(f"[peer connected] || online [{len(self.peers)}]")

    def get_peer_list(self) -> list[str]:
        return list(self.peers.values())

    def get_addr_username(self, peer_addr: tuple[str, int]) -> str:
        return self.peers[peer_addr]


# class Peer:
#     def __init__(self, addr):
#         self.addr = addr