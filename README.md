# OEC Assignment 3


### Running the code:
The following files are required to run the code:
* HeartBeat.py
* Main.py
* NetworkInfo.py

Start the application by running:

```bash
$ python3 Main.py

```

### Starting the node:
When runing the code, the detected network configuration will be displayed. When using a linux system, the IP Address can be disregarded, however when using Windows, make sure the IP Address is correct.
* Press Enter to start running the node.


```
 +-------------------------------+
 | Network Settings              |
 +-------------------------------+
 | IP Address =  10.0.75.1
 | Broadcast  =  255.255.255.255
 | Port       =  50002
 +-------------------------------+

Press enter to start the node or enter an ip address manually:

```

### Monitoring the nodes:

Now you will see information about the connected nodes and the elected master node outputted to the console (refreshed every couple of seconds):
```
 +-------------------------------+
 | Nodes                         |
 +-------------------------------+
 | LAPTOP-MQVKMK1P      : Online
 | LAPTOP-MQVGMK2P      : Online
 | LAPTOP-MQEKMK6P      : Offline
 +-------------------------------+
 | Master:  LAPTOP-MQVKMK1P
 +-------------------------------+

```

### Stopping the node:
* Press Enter again to stop the node.

Do not try to stop the node by pressing Ctrl+C, otherwise the socket will not shutdown properly, and you won't be able to easily start the node again.

