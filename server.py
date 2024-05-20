import socket
import threading

BUFFER_SIZE = 2048
ENCODING = 'utf-8'  # encoding as a constant

class Server:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.usernames = []

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(BUFFER_SIZE)
                self.broadcast(message)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                username = self.usernames[index]
                self.usernames.remove(username)
                self.broadcast(f'{username} left the chat!'.encode(ENCODING))
                break

    def receive(self):
        while True:
            client, address = self.server.accept()

            client.send('USER'.encode(ENCODING))
            username = client.recv(BUFFER_SIZE).decode(ENCODING)
            self.usernames.append(username)
            self.clients.append(client)

            print(f"{username} Connected with the address: {str(address)}")
            self.broadcast(f'{username} joined the chat!'.encode(ENCODING))
            client.send('Connected to the server!'.encode(ENCODING))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

if __name__ == "__main__":
    server = Server()
    server.receive()
