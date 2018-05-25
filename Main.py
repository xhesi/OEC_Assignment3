from HeartBeat import HeartBeat
import NetworkInfo


current_hostname, current_ip, current_broadcast = NetworkInfo.get_network_info()

print(
    "\n",
    "+-------------------------------+", "\n",
    "| Network Settings              |", "\n",
    "+-------------------------------+", "\n",
    "| IP Address = ", current_ip, "\n",
    "| Broadcast  = ", current_broadcast, "\n",
    "| Port       =  50002", "\n",
    "+-------------------------------+", "\n"
      )
current_ip = input('Press enter to start the node or enter an ip address manually:') or current_ip
x = HeartBeat(
    name=current_hostname,
    ip=current_ip,
    broadcast=current_broadcast,
    port=50002,
    heartbeat_interval=2,
    ttl=2,
    debug=False
)
print("Starting Node ...\n")
x.start_receiving()
x.start_sending()
#input('Press enter to manually add node named TestNode:')
#x.add_node("test_Node")
#x.add_node("test_Node2", 15)
input("Press enter to stop server:\n")
x.stop()
