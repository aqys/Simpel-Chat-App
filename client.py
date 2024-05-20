import socket
import threading

BUFFER_SIZE = 2048 
ENCODING = 'utf-8'  # encoding as a constant

class Client:
    def __init__(self, host='127.0.0.1', port=12345):
        self.username = input("Choose your username: ")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def receive(self):
        while True:
            try:
                message = self.client.recv(BUFFER_SIZE).decode(ENCODING)
                if message == 'USER':
                    self.client.send(self.username.encode(ENCODING))
                else:
                    print(message)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                self.client.close()
                break

    def write(self):
        while True:
            message = f'{self.username}: {input("")}'
            self.client.send(message.encode(ENCODING))

    def run(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

if __name__ == "__main__":
    client = Client()
    client.run()
