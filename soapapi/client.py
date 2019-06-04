import socket, ssl

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server


    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket = ssl.wrap_socket(s,
    #                            ca_certs="cert.pem",
    #                            cert_reqs=ssl.CERT_REQUIRED,
    #                            ssl_version=ssl.PROTOCOL_TLSv1)
    # client_socket.connect((host, port))


    message = input(" -> ")  # take input

    while message.lower().strip() != 'exit':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()
