import socket
import threading
import time
import platform
from collections import Counter

class HeartBeat():

    def __init__(self, name, ip='127.0.0.1', broadcast='255.255.255.255', port=50007, heartbeat_interval=10, ttl=10, debug=False):
        threading.Thread.__init__(self)
        # Networking parameters
        self.ip = ip
        self.port = port
        self.broadcast = broadcast
        self.current_platform = platform.system()


        # Socket initialisation
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            if self.current_platform == 'Windows':
                self.serversocket.bind((self.ip, self.port))
            elif self.current_platform == 'Linux':
                self.serversocket.bind(("", self.port))
        except socket.gaierror:
            print("Cannot start node with given IP Address")
            exit(1)
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
        self.debug = debug
        # Lists
        # Status, ttl, time-alive, self-reported-time-alive
        self.nodes = {self.name: [True, 0, 0, 0]}

    def stop(self):
        self.running = False
        print('Exiting Program...')
        self.clientsocket.sendto('exit'.encode(), (self.broadcast, self.port))
        try:
#            self.clientsocket.shutdown(socket.SHUT_WR)
            self.clientsocket.close()
        except Exception as e:
                print("Client Socket: " + str(e))
        try:
#            self.serversocket.shutdown(socket.SHUT_WR)
            self.serversocket.close()
        except Exception as e:
                print("Server Socket:" + str(e))

    def send(self):
        while self.running:
            try:
                message = self.name + "," + str(self.get_age())
                self.clientsocket.sendto(message.encode(), (self.broadcast, self.port))

                time.sleep(self.heartbeat_interval)
                # TODO: Move this code somewhere else
                self.increment_ttl()
                self.master = self.get_oldest_node()
                self.print_status()
            except Exception as e:
                print("Socket Client Send" + str(e))
                self.stop()

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
                if data.decode("utf-8") != 'exit':
                    threading.Thread(target=self.parse_data, args=(data.decode("utf-8"),)).start()
            except:
                pass

    def print_status(self):
        if self.debug is True:
            print(self.nodes)
            print(self.master)
        else:
            print("\n",
                  "+-------------------------------+\n",
                  "| Nodes                         |\n",
                  "+-------------------------------+"
                  )
            for node_key, node_value in self.nodes.items():
                if node_value[0] is True:
                    print(" |", node_key, "\t: Online")
                else:
                    print(" |", node_key, "\t: Offline")
            print(" +-------------------------------+")

    def get_age(self):
        return self.nodes[self.name][2]

    def parse_data(self, data):
        data_list = data.split(",")
        if data_list[0] in self.nodes:
            self.nodes[data_list[0]] = [True, 0, int(self.nodes[data_list[0]][2])+1, int(data_list[1])]
        else:
            self.nodes[data_list[0]] = [True, 0, 0, int(data_list[1])]

    def increment_ttl(self):
        for node_key, node_value in self.nodes.items():
            node_value[1] = node_value[1]+1
            if node_value[1] > self.ttl:
                if not node_key.startswith("test_"):
                    node_value[0] = False
                    node_value[2] = 0
                    node_value[3] = 0

    def get_oldest_node(self):
        oldest_node = [self.name, self.get_age()];
        for node_key, node_value in self.nodes.items():
            if node_key == self.name:
                continue
            elif node_value[3] > oldest_node[1]:
                oldest_node = [node_key, node_value[3]]
        return oldest_node[0]

    def add_node(self, name, age=0):
        if name in self.nodes:
            print("The selected node already exists");
            return False
        else:
            self.nodes[name] = [False, self.ttl+1, 0, age]
            return True


    def remove_node(self, name):
        if name in self.nodes:
            del self.nodes[name]
            return True
        else:
            print("The selected node does not exist");
            return False

