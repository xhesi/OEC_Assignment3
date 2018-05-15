from HeartBeat import HeartBeat
import NetworkInfo

current_ip, current_broadcast = NetworkInfo.get_network_info()

x = HeartBeat(
    name="Me PC",
    ip=current_ip,
    broadcast=current_broadcast,
    port=50001,
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
