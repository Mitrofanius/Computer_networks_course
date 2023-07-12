from logging import DEBUG
# from receiver import BUFF_SIZE
import socket
from zlib import crc32
# from receiver import LOCAL_ADDR, LOCAL_PORT, BUFF_SIZE
import os
# socket.setdefaulttimeout(0.5)

DEST_ADDRESS = ('127.0.0.1', 12000)
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# def establish_connection():
#     client_sock.sendto('SYN', DEST_ADDRESS)

try:
    client_sock.sendto(b"IMG_SENT.png", DEST_ADDRESS)
    ACK = client_sock.recvfrom(1024)
except:
    print("yes")
    exit()

client_sock.sendto(str(os.stat("SF.png").st_size).encode(), DEST_ADDRESS)
ACK = client_sock.recvfrom(1024)

client_sock.sendto(b"Start", DEST_ADDRESS)
ACK = client_sock.recvfrom(1024)


def send_file(DEST_ADDRESS):
    with open("SF.png", 'rb') as f:
        data = f.read(1024)
        while data:
            client_sock.sendto(data, DEST_ADDRESS)
            ACK = client_sock.recvfrom(1024)
            data = f.read(1024)


if __name__ == '__main__':
    send_file(DEST_ADDRESS)


def stop_and_wait(func):
    def wrapper(my_sock, datagram, dest_addr):
        acknowledged = False
        func(datagram, dest_addr)
        while ((not acknowledged) and (ACK == b'ACK')):
            try:
                ACK, address = my_sock.recvfrom(1024)
                acknowledged = True
            except socket.timeout:
                func(datagram, dest_addr)
        return ACK
    return wrapper
