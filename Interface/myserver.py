import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 2000))
server.listen(4)
print("launched")
client_socket, adress = server.accept()
data = client_socket.recv(1024).decode('utf-8')
print(data)

content = "Response given".encode('utf-8')
header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'.encode('utf-8')
client_socket.send(header+content)

print('shutddown')

