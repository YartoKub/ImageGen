import socket
import Request_handler as RH
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
            #print(data)
            main_body, additional_arguments = RH.request_handler(data, adress)
            content = RH.function_picker(main_body, additional_arguments)
            #print(content)
            content = content.encode("utf-8")
            client_socket.send(content)
            client_socket.shutdown(socket.SHUT_WR)
            print('Action Finished')
    except KeyboardInterrupt:
        server.close()
        print("Server down due to keyboard interrupt")

start_server()