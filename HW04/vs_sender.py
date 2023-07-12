# import socket
# import os
# from zlib import crc32
# from hashlib import md5
# from utils_sock import udp_format, Colors
# from time import sleep

# # socket info
# # TARGET_IP = "192.168.30.14"
# TARGET_IP = "127.0.0.1"
# TARGET_PORT = 14000

# DESTINATION_ADDRESS = (TARGET_IP, TARGET_PORT)

# LOCAL_IP = "127.0.0.1"
# LOCAL_PORT = 15001

# LOCAL_ADDRESS = (LOCAL_IP, LOCAL_PORT)
# # ------------------------------------


# # Useless Bohdan's headers
# WINDOW_SIZE = 5
# BUFF_SIZE = 1024
# CRC_SIZE = 10
# INDEX_SIZE = 4
# BYTE_ARRAY_SIZE = 33
# UPD_HEADER_SIZE = 9
# HEADER_SIZE = CRC_SIZE + INDEX_SIZE
# PAYLOAD_SIZE = BUFF_SIZE - HEADER_SIZE - \
#     BYTE_ARRAY_SIZE - UPD_HEADER_SIZE  # 968
# # ------------------------------------------------------------------------------


# def send_stop_and_wait(my_socket, message):
#     acknowledged = False
#     cnt = 0
#     err_cnt_2 = 0

#     while not acknowledged:
#         my_socket.sendto(udp_format(message, 0), DESTINATION_ADDRESS)

#         try:
#             ACK, address = my_socket.recvfrom(BUFF_SIZE)
#             if len(ACK) >= HEADER_SIZE:
#                 return
#             # print(ACK)
#             # if len(ACK) <= HEADER_SIZE:
#             #     continue

#             # print(ACK)
#             # print(ACK[HEADER_SIZE:])
#             if ACK == b"ACK":
#                 acknowledged = True
#                 print(
#                     f"||{Colors.OKGREEN}Acknowledgment has been successfully received.{Colors.ENDC}")
#                 return
#             else:
#                 print(
#                     f"||{Colors.FAIL}Acknowledge ACK is wrong. Sending again...{Colors.ENDC}")
#         except socket.timeout:
#             cnt += 1
#             if cnt == 7:
#                 return
#             continue


# def retransmit(my_socket, buffer, last_acknowledged):
#     print("In retransmit")
#     data = buffer[0][1]
#     my_socket.sendto(udp_format(data, last_acknowledged + 1),
#                      DESTINATION_ADDRESS)


# def update_buffer(buffer, last_ack):
#     to_delete = []
#     print("updating buffer")
#     print(buffer[0][0])

#     for i in range(len(buffer)):
#         if buffer[i][0] <= last_ack:
#             to_delete.append(i)

#     cnt = 0
#     for i in to_delete:
#         buffer.pop(i - cnt)
#         cnt += 1

#     print("updated buffer down there")
#     if len(buffer) > 0:
#         print(buffer[0][0])

#     # return buffer


# def receive_acks(my_socket, buffer, last_acknowledged):
#     print("in recieve acks")
#     while True:
#         print("in recieve acks while")

#         try:
#             msg, addr = my_socket.recvfrom(1024)
#             if len(msg) <= HEADER_SIZE:
#                 continue

#             rec_index = int((msg[HEADER_SIZE:]).decode())

#             if last_acknowledged < rec_index < last_acknowledged + WINDOW_SIZE:
#                 last_acknowledged = rec_index

#         except socket.timeout:
#             return last_acknowledged

#         except ValueError:
#             continue


# def send_file_selective_repeat(my_socket, filename, filesize):
#     file = open(filename, "rb")
#     buffer = []
#     not_sent = True
#     last_acknowledged = -1
#     index = 0
#     num_packs = int(filesize // PAYLOAD_SIZE +
#                     (1 if filesize % PAYLOAD_SIZE != 0 else 0))

#     print("Befor first while")
#     print("")

#     while index < num_packs:
#         while index < last_acknowledged + WINDOW_SIZE:
#             print("Befor first while")
#             print(f"sending acket {index}")
#             print()

#             data = file.read(PAYLOAD_SIZE)
#             buffer.append((index, data))
#             my_socket.sendto(udp_format(data, index), DESTINATION_ADDRESS)
#             index += 1

#         last_acknowledged = receive_acks(my_socket, buffer, last_acknowledged)
#         print(f"last acknowledged = {last_acknowledged}")
#         update_buffer(buffer, last_acknowledged)

#         if index >= last_acknowledged + WINDOW_SIZE:
#             print("In if")
#             print()
#             retransmit(my_socket, buffer, last_acknowledged)

#     file.close()


# if __name__ == "__main__":
#     filename = "BatBegins.jpeg"
#     filesize = os.stat(filename).st_size

#     my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     print("shit")
#     my_socket.bind(LOCAL_ADDRESS)
#     my_socket.settimeout(0.25)

#     # while True:
#     #     my_socket.sendto(b"HEYYEYefghewgveoiEYDYE", DESTINATION_ADDRESS)
#     #     sleep(0.25)

#     send_stop_and_wait(my_socket, filename)
#     send_stop_and_wait(my_socket, filesize)
#     send_stop_and_wait(my_socket, "START")

#     send_file_selective_repeat(my_socket, filename, filesize)
#     send_stop_and_wait(my_socket, "STOP")

#     my_socket.close()

from utils_sock import md5_format
from sender import PAYLOAD_SIZE
import os

filename = "big_sf.jpg"

print(os.stat(filename).st_size / 968)
print(os.stat(filename).st_size)

print(isinstance(md5_format("SF_from_Mitya.jpg").decode(), str))

with open("PSIA.png", "rb") as file:
    x = 10
    print(file.seek(PAYLOAD_SIZE * int(100000000)))
    print(file.tell())
    file.seek(10)
    file.read()
    file.seek(5)
    print(file.tell())
