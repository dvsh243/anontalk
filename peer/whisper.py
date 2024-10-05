def send_whisper(sock, payload: str):
    # extract address & message from payload
    msg = None
    addr = None
    print(f"[whisper to {payload.split(' ')}]")
    # sock.sendto(msg.encode(), addr)