import socket
import threading

BGMI_SERVER_IP = 'BGMI_SERVER_IP'
BGMI_SERVER_PORT = 7777  # Default BGMI server port

def handle_client(connection, address):
    print(f"Connection from {address}")
    while True:
        data = connection.recv(1024)
        if not data:
            break
        print(f"Received data: {data.decode()}")
        connection.sendall(b'BGMI Server: Message received')
    connection.close()
    print(f"Connection closed from {address}")

def start_bgmi_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((BGMI_SERVER_IP, BGMI_SERVER_PORT))
    server.listen(5)
    print(f"BGMI Server started on {BGMI_SERVER_IP}:{BGMI_SERVER_PORT}")

    while True:
        connection, address = server.accept()
        threading.Thread(target=handle_client, args=(connection, address)).start()

# Start the BGMI server
if __name__ == '__main__':
    start_bgmi_server()