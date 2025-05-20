import socket
HEADER200 = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
HEADER404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
PAGE_FOLDER = "ImageGen\Interface\Pages"
my_adress = ('127.0.0.1', 2000)
def start_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(my_adress)
        server.listen(4)
        while True:
            #print("launched")
            client_socket, adress = server.accept()
            data = client_socket.recv(1024).decode('utf-8')
            print(data)
            request_handler(data, adress)
            content = load_page_from_request(data)
            client_socket.send(content)
            client_socket.shutdown(socket.SHUT_WR)
            print('shutddown')
    except KeyboardInterrupt:
        server.close()
        print("Server down due to keyboard interrupt")

def request_handler(request_data, adress): # Эта штука должна определять тип реквеста и вызывать соответствующую функцию наверное из словаря функций?
    print(request_data)
    print(adress)
def load_page_from_request(request_data):
    path = PAGE_FOLDER + request_data.split(" ")[1] 
    response = ''
    try:
        with open(path, "rb") as file:
            response = file.read()
        return HEADER200.encode('utf-8') + response
    except:
        return HEADER404.encode('utf-8') + 'This page does not exist'.encode('utf-8')


    

start_server()