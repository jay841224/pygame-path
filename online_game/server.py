import socket
import _thread

sever = '127.0.0.1'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((sever, port))
except socket.error as e:
    str(e)

s.listen(2)
print('Waiting for a connection, Server started.')

pos = [(0, 0), (100, 100)]

def read_pos(str):
    str = str.split(',')
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ''
    while True:
        try:
            data =read_pos(conn.recv(2048).decode())
            pos[player] = data
            
            
            if not data:
                print('disconnected !')
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print('Received: ', data)
                print('Senfing: ', reply)
            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print('Conneted to: {}'.format(addr))
    _thread.start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1