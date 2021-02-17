from socket import *
import sys
#catch error of not giving an IP Address 
if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

proxySocket = socket(AF_INET, SOCK_STREAM) #create proxy socket 
proxySocket.bind((sys.argv[1], 8888)) #bind proxy socket 
proxySocket.listen(100) #accept up to 100 connections 

while 1:
    print('Ready to server\n')
    conn, addr = proxySocket.accept() #create client connection 

    print('Received a connection from:', addr,'\n')
    request = conn.recv(1024).decode() #get request from client 
    print(request)#print request 

    fileName = request.split()[1].partition("/")[2] #partition the request to just the site name 
    print("File Name: ",fileName,"\n")

    fileExist = False #flag to see if file exist 

    fileToUse = "/"+fileName #name of file to use 
    print("File To use: ",fileToUse,"\n")

    try:
        print("Inside try: ", fileToUse[1:],"\n")
        f = open(fileToUse[1:],"rb") #open file to use in reading bites  mode 
        outputData = f.readlines() # read file into outputdata

        fileExist = True #set flag to file exist true 

        print("Requested file found in cache:", fileToUse)

        conn.send(b"HTTP/1.0 200 OK\r\n") #send a 200 code respond to client
        conn.send(b"Content-Type:text/html\r\n") #send a content type to client 
        for i in range(0, len(outputData)): #read the file and send the data to the client 
            conn.send(outputData[i])
            print('Read from cache')

    except IOError: #catch if the file is not found 
        if not fileExist:
            print("Requested file NOT found in cache, perform GET to server for file:",fileToUse,"\n")

            sock = socket(AF_INET, SOCK_STREAM) #create a new socket to connect to the website 

            host = "www."+fileName #append www. to the start of the fileName
            print("Host: ", host, "\n")

            try:
                sock.connect((host,80)) #connect the socket to the host with prot 80
                request = "GET "+"http://" + host + "/ HTTP/1.0\r\n\r\n" #generate our get request 
                sock.send(request.encode()) # encode and send our request to the wensite 
                buffer = sock.recv(4096) #start to recive info back at 4096 bits

                #tempFile = open("./"+fileName,"wb") 

                while (len(buffer) > 0): #contine to read buffer as long as its not 0
                    # print(buffer.decode())
                    #tempFile.write(buffer)
                    conn.send(buffer) #send info to the client from buffer 
                    buffer = sock.recv(4096) #get the next 4096 bits 
                
            except : #catch any illegal request 
                print("Illegal Request")
        else:
            conn.send(b"HTTP/1.0 404 sendErrorErrorError\r\n")   #send a 404 error to the client                            
            conn.send(b"Content-Type:text/html\r\n") #send a content type to the client 
            conn.send(b"\r\n") #send a new line tp client 
    #Close the client and the server sockets
    # break    
    conn.close() #close client socket 
tcpSerSock.close()#close proxy socket 
    
