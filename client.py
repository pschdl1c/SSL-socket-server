import socket
import threading
import sys
import ssl


class Client:
    def __init__(self, cert_file_name):
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.check_hostname = True
        self.context.load_verify_locations(cert_file_name)

    #Wait for incoming data from server
    def receive(self, socket, signal):
        while signal:
            try:
                data = socket.recv(32)
                print(str(data.decode("utf-8")))
            except:
                print('You have been disconnected from the server.')
                signal = False
                break

    def connect(self, host='localhost', port=10023, server_hostname='localhost'):
        #Attempt connection to server
        try:
            self.socket = self.context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=server_hostname)
            self.socket.connect((host, port))
        except:
            print('Could not make a connection to the server.\nPlease verify the authenticity of the certificate.')
            sys.exit(0)

    def start(self):
        #Create new thread to wait for data
        receiveThread = threading.Thread(target = self.receive, args = (self.socket, True))
        receiveThread.start()
        self.send_message()

    def send_message(self):
            #Send data to server
            while True:
                try:
                    message = input()
                    self.socket.sendall(str.encode(message))
                except KeyboardInterrupt:
                    print('You have logged out of the server.')
                    self.socket.close()
                    break


if __name__ == '__main__':
    host = 'localhost'
    port = 10023
    client = Client('certificates/server.crt')
    client.connect(host, port, 'localhost')
    client.start()