from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.bind((sys.argv[1], 8888))
proxySocket.listen(100)

while 1:
    print('Ready to server\n')
    conn, addr = proxySocket.accept()

    print('Received a connection from:', addr,'\n')
    request = conn.recv(1024).decode()
    print(request)

    fileName = request.split()[1].partition("/")[2]
    print("File Name: ",fileName,"\n")

    fileExist = False

    fileToUse = "/"+fileName
    print("File To use: ",fileToUse,"\n")

    try:
        print("Inside try: ", fileToUse[1:],"\n")
        f = open(fileToUse[1:],"r")
        outputData = f.readlines()

        fileExist = True

        print("Requested file found in cache:", fileToUse)

        conn.send(b"HTTP/1.0 200 OK\r\n")
        conn.send(b"Content-Type:text/html\r\n")
        for i in range(0, len(outputData)):
            conn.send(outputData[i])
            print('Read from cache')

    except IOError:
        if not fileExist:
            print("Requested file NOT found in cache, perform GET to server for file:",fileToUse,"\n")

            sock = socket(AF_INET, SOCK_STREAM)

            host = "www."+fileName
            print("Host: ", host, "\n")

            try:
                sock.connect((host,80))
                request = "GET "+"http://" + host + "/ HTTP/1.0\r\n\r\n"
                sock.send(request.encode())
                buffer = sock.recv(4096)

                tempFile = open("./"+fileName,"wb")

                while (len(buffer) > 0):
                    # print(buffer.decode())
                    tempFile.write(buffer)
                    conn.send(buffer)
                    buffer = sock.recv(4096)
                
                # tempFile = open("./"+fileName,"wb")
                # for line in buff:
                #     print(line)
                #     conn.send(line)
            except :
                print("Illegal Request")
        else:
            conn.send(b"HTTP/1.0 404 sendErrorErrorError\r\n")                             
            conn.send(b"Content-Type:text/html\r\n")
            conn.send(b"\r\n")
    #Close the client and the server sockets
    # break    
    conn.close() 
tcpSerSock.close()
    
