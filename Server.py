import socket
from _thread import *

s = socket.socket()
HOST = '192.168.0.154'
PORT = 5000

try:
    s.bind((HOST,PORT))
except socket.error as e:
    str(e)

s.listen(2)
turn = 0
print("Waiting for connection...")

def threaded_client(conn, player):
    conn.send(str.encode())
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()

while True:
    clientsocket, (ip,port) = s.accept()
    print(f"Connection established: {ip}")
    clientsocket.send(bytes("Welcome to ConnectFour!", 'utf-8'))  # encodes a string into bytes and sends it to client
    name = clientsocket.recv(64)  # recieves a packet of 10 bytes from the client ie the name
    name = name.decode('utf-8')  # decodes the bytes into string format
    print("\nConnecting to ", name, " . . .")
    start_new_thread(threaded_client, (conn, currentPlayer))
    if turn ==0:
        if turn == 0:
            ans = int(input("Please choose a location"))
            print(ans)
        else:
            clientsocket.send(bytes("Please choose a location", 'utf-8'))
            ans = clientsocket.recv(64)
            ans = int(name.decode('utf-8'))
            print(ans)

        turn = turn +1
        turn = turn % 2


