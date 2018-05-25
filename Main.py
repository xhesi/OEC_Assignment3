from HeartBeat import HeartBeat
import NetworkInfo
from collections import Counter
nodes = {'A':[1,2],'B':[3,None],'C':[5,None]}
test= Counter([row[1] for row in nodes.values()][1:]).most_common(1)
print(test[0][0])


current_hostname, current_ip, current_broadcast = NetworkInfo.get_network_info()

print("Using setting:",
    "\nip=", current_ip,
    "\nbroadcast=", current_broadcast,
    "\nport=50002"
      )
input()
x = HeartBeat(
    name=current_hostname,
    ip="",
    broadcast="",
    port=50002,
    heartbeat_interval=2,
    ttl=2,
    test=True
)
print("Starting Node ...")
x.start_receiving()
x.start_sending()
input('Press enter to manually add node named TestNode:')
x.add_node("test_Node")
x.add_node("test_Node2", 15)
input('Press enter to stop server:')
x.stop()
