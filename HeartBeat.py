import socket
import threading
import time
import platform


class HeartBeat:

    def __init__(self, name, ip='127.0.0.1', broadcast='255.255.255.255',
                 port=50007, heartbeat_interval=10, ttl=10, debug=False):

        # Set Networking parameters
        self.ip = ip
        self.port = port
        self.broadcast = broadcast
        self.current_platform = platform.system()

        # Initialize Sockets and bind to IP and port
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

        # Create Thread Containers
        self.receiveThread = None
        self.sendThread = None

        # Set running status
        self.running = True

        # Other parameters
        self.heartbeat_interval = heartbeat_interval
        self.name = name
        self.ttl = ttl
        self.master = self.name
        self.debug = debug

        # Initialize list of nodes
        # Each node conatains the following attributes:
        #                         Status, ttl, time-alive, self-reported-time-alive
        self.nodes = {self.name: [True, 0, 0, 0]}

    def start(self):
        """ Start the node by starting the send and receive threads. """
        self.start_receiving()
        self.start_sending()

    def stop(self):
        """ Set the node state to stopped, closes sockets, and stops the running threads. """
        self.running = False
        print('Exiting Program...')
        self.clientsocket.sendto('exit'.encode(), (self.broadcast, self.port))
        try:
            self.clientsocket.close()
        except Exception as e:
                print("Client Socket: " + str(e))
        try:
            self.serversocket.close()
        except Exception as e:
                print("Server Socket:" + str(e))

    def send(self):
        """ Broadcast the nodes own name and time-alive as a UDP message. Increments ttl of all nodes,
        and sets the master. """
        while self.running:
            try:
                message = self.name + "," + str(round(self.get_age()*self.heartbeat_interval)) + "," + self.master
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
        """ Start the receive method in its own thread. """
        self.receiveThread = threading.Thread(target=self.receive)
        self.receiveThread.start()

    def start_sending(self):
        """ Starts the send method in its own thread. """
        self.sendThread = threading.Thread(target=self.send)
        self.sendThread.start()

    def receive(self):
        """ Receive data from the bound socket and start a new thread for parsing the data. """
        while self.running:
            try:
                data, addr = self.serversocket.recvfrom(1024)  # buffer size is 1024 bytes
                if data.decode("utf-8") != 'exit':
                    threading.Thread(target=self.parse_data, args=(data.decode("utf-8"),)).start()
            except:
                pass

    def print_status(self):
        """ Prints the status of the nodes and the current master in a nicely formatted ASCII UI. """
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
            print(" +-------------------------------+\n",
                  "| Master: ", self.master, "\n",
                  "+-------------------------------+"
                  )

    def get_age(self):
        """ Returns the age of the current node in terms of heartbeats."""
        return self.nodes[self.name][2]

    def parse_data(self, data):
        """ Parses the data received from the other nodes and adjusts the nodes table. """
        data_list = data.split(",")
        if data_list[0] in self.nodes:
            self.nodes[data_list[0]] = [True, 0, int(self.nodes[data_list[0]][2])+1, int(data_list[1])]
        else:
            self.nodes[data_list[0]] = [True, 0, 0, int(data_list[1])]

    def increment_ttl(self):
        """ Increments the TTL of all nodes, and sets the nodes
        as offline if the TTL is above the specified threshhold. """
        for node_key, node_value in self.nodes.items():
            node_value[1] = node_value[1]+1
            if node_value[1] > self.ttl:
                if not node_key.startswith("test_"):
                    node_value[0] = False
                    node_value[2] = 0
                    node_value[3] = 0

    def get_oldest_node(self):
        """ Returns the node with the highest self-reported time-alive"""
        oldest_node = [self.name, round(self.get_age()*self.heartbeat_interval)];
        for node_key, node_value in self.nodes.items():
            if node_key == self.name:
                continue
            elif node_value[3] > oldest_node[1]:
                oldest_node = [node_key, node_value[3]]
            elif node_value[3] == oldest_node[1]:
                # In case of same age, choose the first sorted alphabetically
                if node_key < oldest_node[0]:
                    oldest_node = [node_key, node_value[3]]
        return oldest_node[0]

    def add_node(self, name, age=0):
        """ Adds a node to the list of nodes. """
        if name in self.nodes:
            print("The selected node already exists");
            return False
        else:
            self.nodes[name] = [False, self.ttl+1, 0, age]
            return True

    def remove_node(self, name):
        """ Removes a node from the list of nodes. """
        if name in self.nodes:
            del self.nodes[name]
            return True
        else:
            print("The selected node does not exist");
            return False

