import socket

HOST = "localhost"
PORT = 8081

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

sock.sendall(("Hello\n").encode("utf-8"))
data = sock.recv(1024)
print("1)", data)

if (data == "olleH\n"):
    sock.sendall("Bye\n")
    data = sock.recv(1024)
    print("2)", data)

    if (data == "eyB}\n"):
        sock.close()
        print("Socket closed")