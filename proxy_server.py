import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1" #IP 
PROXY_SERVER_PORT = 8080

# send some data(request) to host:port
def send_request(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.send(request)
        # shut the socket to further writes. Tells server we're done sending
        client_socket.shutdown(socket.SHUT_WR)

        # Assemble response, be careful, recall that recv(bytes) block until it receives data
        data = client_socket.recv(BYTES_TO_READ)
        result = b''+data
        while len(data)>0:
            data = client_socket.recv(BYTES_TO_READ)
            result+=data
        
        # Return response
        return data

# Handling an incoming connection that has been accepted by the server
def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")

        request = b''
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print("Proxy server get data: ", data)
            request += data
        respense = send_request("www.google.com", 80, request)  # send as a request to www.google.com   proxy--->server
        conn.sendall(respense)  # return the response from www.google.com back to the client   client<---proxy

# Start single-thread proxy server
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST,PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)  # Allowing queing up to 2 connections
        conn, addr = server_socket.accept()
        handle_connection(conn, addr)  # eg: client's conn, addr

# Start multiple_threaded proxy server
def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST,PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)  # Allowing queing up to 2 connections
        while True:
            conn, addr = server_socket.accept()
            thread = Thread(target=handle_connection, args=(conn,addr))
            thread.run()

start_threaded_server()








