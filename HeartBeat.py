import socket
import threading

class HeartBeat():

    def __init__(self, ip='127.0.0.1', broadcast='127.0.0.1', port=50007):
        threading.Thread.__init__(self)
        print('__init__ called')
        self.ip = ip
        self.port = port
        self.broadcast = broadcast
        print(self.ip)
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serversocket.bind((self.broadcast, self.port))
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiveThread = None
        self.running = True

    def stop(self):
        self.running = False
        print('stop called')
        self.receiveThread.join()
        self.serversocket.close()
        self.clientsocket.close()


    def send(self):
        message = "Hello, World!"
        self.clientsocket.sendto(message.encode(), (self.broadcast, self.port))
        self.clientsocket.shutdown(socket.SHUT_WR)

    def startReceiving(self):
        self.receiveThread = threading.Thread(target=self.receive)
        self.receiveThread.start()

    def receive(self):
        while self.running:
            data, addr = self.serversocket.recvfrom(1024)  # buffer size is 1024 bytes
            print("received message:", data, " from : ", addr)
