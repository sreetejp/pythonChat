import socket
from threading import Thread


def listen_for_client(cs, separator):
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            msg = msg.replace(separator, ": ")
        for client_socket in client_sockets:
            client_socket.send(msg.encode())


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5184
separator_token = "<SEP>"

client_sockets = set()

with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    while True:
        try:
            client_socket, client_address = s.accept()
        except Exception as e:
            print(f"[!] Error: {e}")
        else:
            print(f"[+] {client_address} connected.")
            client_sockets.add(client_socket)
            t = Thread(target=listen_for_client, args=(client_socket, separator_token))
            t.daemon = True
            t.start()
