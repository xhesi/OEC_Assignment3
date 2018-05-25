from HeartBeat import HeartBeat
import NetworkInfo

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

# Initialize Node
node = HeartBeat(
    name=current_hostname,
    ip=current_ip,
    broadcast=current_broadcast,
    port=port,
    heartbeat_interval=2,
    ttl=2,
    debug=False
)

# Start Node
print("Starting Node ...\n")
node.start()

# Stop Node
input("Press enter to stop server:\n")
node.stop()
