import select
import socket
from time import sleep

LOCAL_IP = "127.0.0.1"
LOCAL_PORT = 5555
addr = (LOCAL_IP, LOCAL_PORT)


my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_sock.bind(addr)
my_sock.settimeout(10)


sleep(5)

r, w, e = select.select([my_sock], [my_sock], [my_sock])
print(r)
print(w)
print(e)

msg, targ = my_sock.recvfrom(1024)
my_sock.sendto(msg, targ)

for i in range(4):
    print(my_sock.recvfrom(1024))
print("done")
