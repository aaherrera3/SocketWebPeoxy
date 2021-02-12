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
    print('+++++++++++++++++++++++++++++++++++')
    fileName = request.split()[1].partition("/")[2]
    
    fileExist = False

    filetouse = "/"+fileName

    print(filetouse)

    try:
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = True
        Print("Requested file found in cache:", filetouse)
        proxySocket.send("HTTP/1.0 200 OK\r\n")            
        proxySocket.send("Content-Type:text/html\r\n")
        for i in range(0, len(outputdata)):             
            proxySocket.send(outputdata[i])
            print('Read from cache')
    except IOError:
        if not fileExist:
            print("Requested file not found in cache, performing Get to server for file:", filetouse)
            sock = socket(AF_INET, SOCK_STREAM)
            host = fileName.replace("www.","",1)
            print(host)
            try:
                sock.connect((host,80))
                fileMake = scok.makefile('r',0)
                fileMake.write("GET "+"http://" + fileName + " HTTP/1.0\n\n")
                buffer = fileMake.readlines()
                tempFile = open("./"+fileName, "wb")
                for line in buffer:
                    tempFile.write(line)
                    proxySocket.send(line)
            except:
                print("Illegal request")
        else:
            proxySocket.send("HTTP/1.0 404 sendErrorErrorError\r\n")                             
            proxySocket.send("Content-Type:text/html\r\n")
            proxySocket.send("\r\n")
        break

    
