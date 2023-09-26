import socket
from threading import Thread

BYTES_TO_READ = 4096
HOST = "127.0.0.1" #IP 
PORT  = 8080

def handle_connections(conn, addr):
    """
    conn: client socket
    addr: Client IP
    """
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(BYTES_TO_READ)  # Wait for a connection, and when get it , receive 
            if not data:
                break
            print("Data received: ", data)
            conn.sendall(data)   # server send all data readed

# Start single threaded echo server
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))  # able to accept incoming connection on the ip and port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)  # This option allows to reuse a local address that is already in use( shut down and restart quickly)
        s.listen()  # listen for the incoming connections
        conn, addr = s.accept()  # Accept the client connection conn = client socket, addr = client Ip
        print(addr)
        handle_connections(conn, addr)  # Send response

def start_threade_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))  # able to accept incoming connection on the ip and port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)  # This option allows to reuse a local address that is already in use( shut down and restart quickly)
        s.listen(2)  # Allow backlog of up to 2 connections ==> queue [waiting 1, waiting 2]
        while True:
            conn, addr = s.accept()  # Accept the client connection conn = client socket, addr = client Ip
            print(addr)
            thread = Thread(target=handle_connections, args=(conn, addr))
            thread.run()

start_threade_server()
    


