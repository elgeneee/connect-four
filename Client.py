import socket

c = socket.socket()
HOST = '172.20.10.2'
PORT = 5000

c.connect((HOST,PORT))

# msg=c.recv(64)                          # recieves a packet of 64 bytes from server
# print(msg.decode('utf-8'))              # decodes bytes into string
# name1 = "Elgene"
# c.send(bytes(name1.encode('utf-8')))

while True:
    msg = c.recv(64)
    print(msg.decode('utf-8'))
    ans = input()
    c.send(bytes(ans.encode('utf-8')))