import socket

TARGET_IP = "127.0.0.1"
TARGET_PORT = 5555

targ = (TARGET_IP, TARGET_PORT)

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

my_sock.sendto(b"DAMN", targ)
my_sock.sendto(b"SHIT", targ)
my_sock.sendto(b"SHIT", targ)
my_sock.sendto(b"SHIT", targ)
my_sock.sendto(b"SHIT", targ)
