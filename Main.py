from HeartBeat import HeartBeat
import threading
import time


x = HeartBeat(
    name = "Me",
    ip='127.0.0.1',
    broadcast='127.0.0.1',
    port=50001,
    heartbeat_interval=2,
    ttl=10
)
x.start_receiving()
print("hi")
x.start_sending()
input('Press enter to manually add node named TestNode:')
x.add_node("TestNode")
input('Press enter to stop server:')
x.stop()