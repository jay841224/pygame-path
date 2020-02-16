import socket
import _thread

sever = '192.168.11.104'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((sever, port))
except socket.error as e:
    str(e)

s.listen(2)
print('Waiting for a connection, Server started.')

def threaded_client(conn):
    conn.send(str.encode('Connected'))
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                print('disconnected !')
                break
            else:
                print('Received: ', reply)
                print('Senfing: ', reply)
            conn.sendall(str.encode(reply))
        except:
            break

while True:
    conn, addr = s.accept()
    print('Conneted to: {}'.format(addr))
    _thread.start_new_thread(threaded_client, (conn,))