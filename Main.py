from HeartBeat import HeartBeat
import NetworkInfo
import time

# Get Network Settings
current_hostname, current_ip, current_broadcast = NetworkInfo.get_network_info()
port = 50002
print(
    "\n",
    "+-------------------------------+", "\n",
    "| Network Settings              |", "\n",
    "+-------------------------------+", "\n",
    "| IP Address = ", current_ip, "\n",
    "| Broadcast  = ", current_broadcast, "\n",
    "| Port       = ", port, "\n",
    "+-------------------------------+", "\n"
      )
current_ip = input('Press enter to start the node or enter an ip address manually:') or current_ip
continue_flag="continue"
# Initialize Node
while continue_flag != "exit":
  node = HeartBeat(
    name=current_hostname,
    ip=current_ip,
    broadcast=current_broadcast,
    port=port,
    heartbeat_interval=2,
    ttl=2,
    debug=False
)
## Start Node
  print("Starting Node ...\n")
#while continue_flag:
  try:
    node.start()
# Stop Node
    continue_flag=input("Type exit and press enter to stop server:\n")
#    continue_flag=False
    node.stop()
  except Exception as e:
    print("Restarting program because interface is offline")
    node.stop()
    time.sleep(2)
    
