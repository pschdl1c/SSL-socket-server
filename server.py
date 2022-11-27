import socket
import threading
import ssl

#Constants for holding information about connections
connections = []
total_connections = 0

class Client(threading.Thread):
    def __init__(self, socket, address, _id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = _id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return f'{str(self.id)} {str(self.address)}'
    
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
            except:
                print(f'Client {str(self.address)} has disconnected')
                self.signal = False
                connections.remove(self)
                break
            if data != "":
                print(f'ID {str(self.id)}: {str(data.decode("utf-8"))}')
                if data.decode("utf-8") == '/list':
                    for client in connections:
                        if client.id != self.id:
                            client.socket.sendall(data)
                else:
                    for client in connections:
                        if client.id != self.id:
                            client.socket.sendall(str.encode(f'Name: {self.name} - ') + data)

class Server:
    def __init__(self, cert_filename, key_filename):
        print('Starting the server')
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=cert_filename, keyfile=key_filename)
        print('[SYSTEM] The server is running')

    def start(self, host='localhost', port=10023):
        #Create new server socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(5)
        self.thread_connection(sock)

    #Wait for new connections
    def newConnections(self, socket):
        while True:
            sock, address = socket.accept()
            try:
                wrapped_socket = self.context.wrap_socket(sock, server_side=True)
                name = wrapped_socket.recv(32).decode("utf-8")
                global total_connections
                connections.append(Client(wrapped_socket, address, total_connections, name, True))
                connections[len(connections) - 1].start()
                print(f'New connection at ID {str(connections[len(connections) - 1])}, Name: {name}')
                total_connections += 1
            except:
                print(f'[ALERT] The client {address} has an unknown SSL certificate')

    def thread_connection(self, server_socket):
        #Create new thread to wait for connections
        newConnectionsThread = threading.Thread(target = self.newConnections, args = (server_socket,))
        newConnectionsThread.start()


if __name__ == '__main__':
    server = Server("certificates/server.crt", "certificates/server.key")
    server.start('localhost', 10023)