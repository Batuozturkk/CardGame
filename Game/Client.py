import socket
import threading

HOST = 'localhost'  # Replace with the server's IP address
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def receive_data():
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            print("Received data:", data)

receive_thread = threading.Thread(target=receive_data)
receive_thread.start()

while True:
    message = input("Enter a message to send to the server: ")
    client_socket.send(message.encode('utf-8'))

client_socket.close()