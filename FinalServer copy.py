import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 2020
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

connectedClients = []

def handle_client(conn, addr):
    msg = conn.recv(SIZE).decode(FORMAT)
    if msg.split(' ')[1] in connectedClients:
        msg = "ERROR! User Already Exists, Try Other Name!"
        conn.send(msg.encode(FORMAT))
        conn.close()
    else:
        connectedClients.append(msg.split(' ')[1])
        msg = "OK! Connected to Server!"
        conn.send(msg.encode(FORMAT))

        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            msg = conn.recv(SIZE).decode(FORMAT)
            if msg.lower() == 'disconnect':
                connected = False
                print(f"[{addr}] {msg}")
                msg = f"OK! Disconnected from Server!"
                conn.send(msg.encode(FORMAT))

            elif msg.lower() == 'lu':
                msg = f"List of Users: {connectedClients}"
                conn.send(msg.encode(FORMAT))

            elif msg.lower() == 'lf':
                filesList = os.listdir("FilesOnServer\\")
                msg = f"List of Files on Server: {filesList}"
                conn.send(msg.encode(FORMAT))

            elif 'read' == msg.lower().split(' ')[0] and len(msg.lower().split(' '))==2:
                fileName = msg.split(' ')[1]
                if fileName in os.listdir("FilesOnServer\\"):
                    with open(f"FilesOnServer\\{fileName}", 'r') as file:
                        msg = file.read()
                    fileSize = os.path.getsize(f"FilesOnServer\\{fileName}")
                    conn.send(f"File Size: {fileSize}\nFile Data: {msg}".encode(FORMAT))
                else:
                    msg = f"ERROR! File Not Found!"
                    conn.send(msg.encode(FORMAT))

            elif 'write' == msg.lower().split(' ')[0] and len(msg.lower().split(' ')) == 2:
                fileName = msg.split(' ')[1]
                if fileName in os.listdir("FilesOnServer\\"):
                    msg = f"ERROR! File Already Exists!"
                    conn.send(msg.encode(FORMAT))
                else:
                    msg = f"OK!"
                    conn.send(msg.encode(FORMAT))
                    msg = conn.recv(SIZE).decode(FORMAT)
                    with open(f"FilesOnServer\\{fileName}", 'w') as file:
                        file.write(msg)
                    msg = f"OK! File Written!"
                    conn.send(msg.encode(FORMAT))

            elif 'overwrite' == msg.lower().split(' ')[0] and len(msg.lower().split(' ')) == 2:
                fileName = msg.split(' ')[1]
                if fileName in os.listdir("FilesOnServer\\"):
                    msg = f"OK!"
                    conn.send(msg.encode(FORMAT))
                    msg = conn.recv(SIZE).decode(FORMAT)
                    with open(f"FilesOnServer\\{fileName}", 'w') as file:
                        file.write(msg)
                    msg = f"OK! File Overwritten!"
                    conn.send(msg.encode(FORMAT))
                else:
                    msg = f"ERROR! File Not Found!"
                    conn.send(msg.encode(FORMAT))

            elif 'append' == msg.lower().split(' ')[0] and len(msg.lower().split(' ')) == 2:
                fileName = msg.split(' ')[1]
                if fileName in os.listdir("FilesOnServer\\"):
                    msg = f"OK!"
                    conn.send(msg.encode(FORMAT))
                    msg = conn.recv(SIZE).decode(FORMAT)
                    with open(f"FilesOnServer\\{fileName}", 'a') as file:
                        file.write(msg)
                    msg = f"OK! File Appended!"
                    conn.send(msg.encode(FORMAT))
                else:
                    msg = f"ERROR! File Not Found!"
                    conn.send(msg.encode(FORMAT))

            elif 'append' == msg.lower().split(' ')[0] and len(msg.lower().split(' ')) == 3:
                fileName = msg.split(' ')[1]
                if fileName in os.listdir("FilesOnServer\\"):
                    msg = f"OK!"
                    conn.send(msg.encode(FORMAT))
                    msg = conn.recv(SIZE).decode(FORMAT)
                    with open(f"FilesOnServer\\{fileName}", 'a') as file:
                        file.write(msg)
                    msg = f"OK! File Appended!"
                    conn.send(msg.encode(FORMAT))
                else:
                    msg = f"ERROR! File Not Found!"
                    conn.send(msg.encode(FORMAT))

        conn.close()


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    main()
