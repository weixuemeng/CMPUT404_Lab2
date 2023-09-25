import socket
BYTES_TO_READ = 4096

def get(host, port):
    request = b"GET / HTTP/1.1\nHost: "+host.encode('utf-8')+b"\n\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Open up a socket : IPV4, TCP 
    s.connect((host,port))
    s.send(request)
    s.shutdown(socket.SHUT_WR)

    chunk = s.recv(BYTES_TO_READ) # keeps reading incoming data
    result = b''+chunk

    while len(chunk)>0:
        chunk = s.recv(BYTES_TO_READ)
        result+= chunk

    s.close()
    return result

print(get("localhost", 8080))
