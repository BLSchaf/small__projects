import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '192.168.1.223'
        self.port = 9999
        self.address = (self.server, self.port)
        self.player = self.connect()

    def get_player(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.address)
            print('connecting...')
            return self.client.recv(2048).decode()

        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(str.encode(data)) # e.g. send 'Rock'
            return pickle.loads(self.client.recv(2048)) # whole game state (object)
        except socket.error as e:
            print(e)
