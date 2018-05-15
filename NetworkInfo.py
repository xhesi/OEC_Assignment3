import socket
import subprocess
import platform
import ipaddress

def get_network_info():
    hostname = socket.gethostname()
    current_platform = platform.system()
    ip = socket.gethostbyname(socket.gethostname())
    if current_platform == 'Windows':
        # Windows
        proc = subprocess.Popen('ipconfig', stdout=subprocess.PIPE)
        while True:
            line = proc.stdout.readline()
            if ip.encode() in line:
                break
        mask = proc.stdout.readline().rstrip().split(b':')[-1].replace(b' ', b'').decode()
    elif current_platform == 'Linux':
        # Unix
        proc = subprocess.Popen('ifconfig', stdout=subprocess.PIPE)
        while True:
            line = proc.stdout.readline()
            if ip.encode() in line:
                break
        mask = line.rstrip().split(b':')[-1].replace(b' ', b'').decode()
    broadcast = str(ipaddress.IPv4Network(ip + '/' + mask, False).broadcast_address)

    return hostname, ip, broadcast


