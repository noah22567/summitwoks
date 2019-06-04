import socket
from mylib.findstr import ftstr
from mylib.fib import fibs
import os

def runserver():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    log = open('.\log.txt', 'a')
    log.write("connected to %s : %s \n" % (host , address ))

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        print("from connected user: " + str(data))

        if str(data) == 'quitserver' :  # will make an exit command for server
            # if data is not received break
            break

        if str(data) == 'reset':
            xml = open("templates/tests.xml", 'w')
            xml.write('<?xml version="1.0" encoding="UTF-8"?>\n \
                     <shiporder orderid="889923"\n\
                     xmlns:xsi="127.0.0.1"\n\
                     xsi:noNamespaceSchemaLocation="fib.xsd">')
            xml.close()


        try:
            command, num = ftstr(data)

            if str(command) == 'fib':
                data = "go to http://127.0.0.1:8000/templates/tests.xml to see the output, and 'reset' to start over)"
                conn.send(data.encode())
                xml = open("templates/tests.xml", 'a')
                nums = set(fibs(int(num)))
                for n in nums:
                    xml.write('<num>'+str(n)+'</num> \n')
                xml.close()
            else:
                continue
        except:
            continue
            # os.system("python -m http.server -b 127.0.0.1")


  # send data to the client


    conn.close()  # close the connection


if __name__ == '__main__':
    runserver()
