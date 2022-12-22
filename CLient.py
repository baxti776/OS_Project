import socket

# Client
IP = socket.gethostbyname(socket.gethostname())
PORT = 2020
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"


def main():
    command = input(">")

    if len(command.split(' ')) == 2 and 'connect' == command.lower().split()[0]:

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        # print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

        msg = command.lower()
        client.send(msg.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")

        if msg == "OK! Connected to Server!":
            connected = True
            while connected:
                msg = input("> ")
                client.send(msg.encode(FORMAT))
                if msg == 'OK! Disconnected from Server!':
                    connected = False
                    print(f"[SERVER] {msg}")
                else:
                    if 'write' == msg.lower().split(' ')[0] and len(msg.lower().split(' ')) == 2:
                        msgSub = client.recv(SIZE).decode(FORMAT)
                        if msgSub == "OK!":
                            with open(f"FilesOnClient\\{msg.split(' ')[1]}", 'r') as file:
                                msg = file.read()
                            client.send(msg.encode(FORMAT))
                        else:
                            print(f"[SERVER] {msgSub}")
                            continue
                    elif 'overwrite' == msg.lower().split(' ')[0] and len(msg.lower().split(' ')) == 2:
                        msgSub = client.recv(SIZE).decode(FORMAT)
                        if msgSub == "OK!":
                            with open(f"FilesOnClient\\{msg.split(' ')[1]}", 'r') as file:
                                msg = file.read()
                            client.send(msg.encode(FORMAT))
                        else:
                            print(f"[SERVER] {msgSub}")
                            continue
                    elif 'append' == msg.lower().split(' ')[0] and len(msg.lower().split(' ')) == 2:
                        msgSub = client.recv(SIZE).decode(FORMAT)
                        if msgSub == "OK!":
                            msg = input("Enter Data to Append: ")
                            client.send(msg.encode(FORMAT))
                        else:
                            print(f"[SERVER] {msgSub}")
                            continue

                    elif 'append' == msg.lower().split(' ')[0] and len(msg.lower().split(' ')) == 3:
                        msgSub = client.recv(SIZE).decode(FORMAT)
                        if msgSub == "OK!":
                            with open(f"FilesOnClient\\{msg.split(' ')[2]}", 'r') as file:
                                msg = file.read()
                            client.send(msg.encode(FORMAT))
                        else:
                            print(f"[SERVER] {msgSub}")
                            continue
                    msg = client.recv(SIZE).decode(FORMAT)
                    print(f"[SERVER] {msg}")

    else:
        print("Invalid Command")


if __name__ == "__main__":
    main()
