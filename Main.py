from HeartBeat import HeartBeat
import NetworkInfo

current_hostname, current_ip, current_broadcast = NetworkInfo.get_network_info()

print("Using setting:",
    "\nip=", current_ip,
    "\nbroadcast=", current_broadcast,
    "\nport=50002"
      )

x = HeartBeat(
    name=current_hostname,
    ip=current_ip,
    broadcast=current_broadcast,
    port=50002,
    heartbeat_interval=2,
    ttl=2
)
print("Starting Node ...")
x.start_receiving()
x.start_sending()
input('Press enter to manually add node named TestNode:')
x.add_node("TestNode")
input('Press enter to stop server:')
x.stop()
