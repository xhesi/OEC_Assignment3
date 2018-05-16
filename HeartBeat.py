import socket
import threading
import time
from collections import Counter

class HeartBeat():

    def __init__(self, name, ip='127.0.0.1', broadcast='255.255.255.255', port=50007, heartbeat_interval=10, ttl=10, test=False):
        threading.Thread.__init__(self)
        # Networking parameters
        self.ip = ip
        self.port = port
        self.broadcast = broadcast


        # Socket initialisation
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serversocket.bind((self.ip, self.port))
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.receiveThread = None
        self.sendThread = None
        self.running = True

        # Other parameters
        self.heartbeat_interval = heartbeat_interval
        self.name = name
        self.ttl = ttl
        self.master = self.name
        self.nomination = self.name
        self.test = test
        # Lists
        # Status, ttl, time-alive, nomination, master-election
        self.nodes = {self.name: [True, 0, 0, self.nomination, self.master]}

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
                self.nominate()
                message = self.name + "," + self.get_oldest_node() + "," + self.nomination
                self.clientsocket.sendto(message.encode(), (self.broadcast, self.port))
                if self.test:
                    self.clientsocket.sendto(message.encode(), (self.broadcast, 50001))
                    self.clientsocket.sendto(message.encode(), (self.broadcast, 50002))
                    self.clientsocket.sendto(message.encode(), (self.broadcast, 50003))
                    self.clientsocket.sendto(message.encode(), (self.broadcast, 50004))
                time.sleep(self.heartbeat_interval)
                # TODO: Move this code somewhere else
                self.increment_ttl()

                self.elect_master()
                print(self.nodes)
                print(self.master)
            except Exception as e:
                print(e)

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
        data_list=data.split(",")
        if data_list[0] in self.nodes:
            self.nodes[data_list[0]] = [True, 0, self.nodes[data_list[0]][2]+1, data_list[1], data_list[2]]
        else:
            self.nodes[data_list[0]] = [True, 0, 0, data_list[1], data_list[2]]

    def increment_ttl(self):
        for node_key, node_value in self.nodes.items():
            node_value[1] = node_value[1]+1
            if node_value[1] > self.ttl:
                node_value[0] = False
                node_value[2] = 0
                node_value[3] = None

    def get_oldest_node(self):
        oldest_node = [self.name, 0];
        for node_key, node_value in self.nodes.items():
            if node_key == self.name:
                continue
            elif node_value[2] > oldest_node[1]:
                oldest_node = [node_key, node_value[2]]
        return oldest_node[0]

    def nominate(self):
        if len(self.nodes) > 2:
            value = Counter([row[3] for row in self.nodes.values()][1:]).most_common(1)
            if value[0][0] is None:
                self.nomination = self.name;
            else:
                self.nomination = value[0][0];
        elif len(self.nodes) == 2:
                tmp = list(self.nodes.values())[1][3]
                if tmp is not None:
                    self.nomination = tmp
                else:
                    self.nomination = self.name

    def elect_master(self):
        if len(self.nodes) > 1:
            value = Counter([row[4] for row in self.nodes.values()]).most_common(1)
            if value[0][0] is not None:
                self.master = value[0][0];


    def add_node(self, name):
        if name in self.nodes:
            print("The selected node already exists");
            return False
        else:
            self.nodes[name] = [False, self.ttl+1, 0, None, None]
            return True

    def remove_node(self, name):
        if name in self.nodes:
            del self.nodes[name]
            return True
        else:
            print("The selected node does not exist");
            return False
