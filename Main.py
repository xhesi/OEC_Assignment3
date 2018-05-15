from HeartBeat import HeartBeat
import NetworkInfo
from collections import Counter

#input_dict = {'A': [45, None], 'B': [45, None], 'C': [45, 1966]}

#value, count = Counter([row[1] for row in input_dict.values()]).most_common(2)
#print(value)
#exit()
current_hostname, current_ip, current_broadcast = NetworkInfo.get_network_info()

x = HeartBeat(
    name=current_hostname,
    ip=current_ip,
    broadcast=current_broadcast,
    port=50002,
    heartbeat_interval=2,
    ttl=10
)
print("Starting Node ...")
x.start_receiving()
x.start_sending()
input('Press enter to manually add node named TestNode:')
x.add_node("TestNode")
input('Press enter to stop server:')
x.stop()
