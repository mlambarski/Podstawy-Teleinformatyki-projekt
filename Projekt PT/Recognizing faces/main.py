import socket

class receive_message:
    def __init__(self):
        TCP_IP = "192.168..101"
        TCP_PORT = 50001
        self.BUFFER_SIZE = 1024
        self.sock = socket.socket(socket.AF_INET,  # Internet
                            socket.SOCK_STREAM)  # TTCP
        self.sock.bind((TCP_IP, TCP_PORT))
        self.sock.listen(1)

        self.conn, self.addr = self.sock.accept()

    def listening(self):
        while True:
            data = self.conn.recv(self.BUFFER_SIZE)  # buffer size is 1024 bytes
            if not data: break
            print("received message:", data)
            self.conn.send(data)

r = receive_message()
r.listening()