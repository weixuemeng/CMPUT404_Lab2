import socket
BYTES_TO_READ = 4096

def get(host, port):  
    """
    host: target(server) socket
    port: port to connect to
    """
    request = b"GET / HTTP/1.1\nHost: "+host.encode('utf-8')+b"\n\n"  # request
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Open up a socket : IPV4, TCP 
    s.connect((host,port))
    s.send(request)
    s.shutdown(socket.SHUT_WR)
    result = s.recv(BYTES_TO_READ) # keeps reading incoming data (from the socket)
    while len(result)>0:
        print(result)
        result = s.recv(BYTES_TO_READ)

    s.close()

get("localhost", 8080)
