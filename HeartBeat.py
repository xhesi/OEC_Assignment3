import socket
import threading
import time


class HeartBeat():

    def __init__(self, name, ip='127.0.0.1', broadcast='127.0.0.1', port=50007, heartbeat_interval=10, ttl=10):
        threading.Thread.__init__(self)
        # Networking parameters
        self.ip = ip
        self.port = port
        self.broadcast = broadcast


        # Socket initialisation
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serversocket.bind((self.ip, self.port))
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiveThread = None
        self.sendThread = None
        self.running = True

        # Other parameters
        self.heartbeat_interval = heartbeat_interval
        self.name = name
        self.ttl = ttl
        # Lists
        self.nodes = {self.name: [True, 0]}

    def stop(self):
        self.running = False
        self.clientsocket.shutdown(socket.SHUT_WR)
        self.serversocket.shutdown(socket.SHUT_WR)
        print('Exiting Program...')
        self.serversocket.close()
        self.clientsocket.close()

    def send(self):
        while self.running:
            try:
                message = self.name
                self.clientsocket.sendto(message.encode(), (self.broadcast, self.port))
                time.sleep(self.heartbeat_interval)
                # TODO: Move this code somewhere else
                self.increment_ttl()
                print(self.nodes)
            except:
                pass

    def start_receiving(self):
        self.receiveThread = threading.Thread(target=self.receive)
        self.receiveThread.start()

    def start_sending(self):
        self.sendThread = threading.Thread(target=self.send)
        self.sendThread.start()

    def receive(self):
        while self.running:
            try:
                data, addr = self.serversocket.recvfrom(1024)  # buffer size is 1024 bytes
                #print("received message:", data, " from : ", addr[0])
                threading.Thread(target=self.parse_data, args=(data.decode("utf-8"),)).start()
            except:
                pass

    def parse_data(self, data):
        self.nodes[data] = [True, 0]

    def increment_ttl(self):
        for node_key, node_value in self.nodes.items():
            node_value[1] = node_value[1]+1
            if node_value[1] > self.ttl:
                node_value[0] = False

    def add_node(self,name):
        if name in self.nodes:
            print("The selected node already exists");
            return False
        else:
            self.nodes[name] = [True, self.ttl+1]
            return True

    def remove_node(self,name):
        if name in self.nodes:
            del self.nodes[name]
            return True
        else:
            print("The selected node does not exist");
            return False
