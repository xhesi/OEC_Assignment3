from HeartBeat import HeartBeat
import threading
import time


x = HeartBeat('127.0.0.1', '127.0.0.1', 50008)
x.startReceiving()
print("hi")
x.send()
input('Press enter to stop server:')
x.stop()
