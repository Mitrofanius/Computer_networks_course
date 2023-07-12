import logging
import sys
from os import sendfile, stat_result
import socket
from zlib import crc32
import os
import hashlib


def md5_hash(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


logging.basicConfig(level=logging.INFO)

TARGET_ADDR = '192.168.30.19'
TARGET_PORT = 14001
DEST_ADDR = (TARGET_ADDR, TARGET_PORT)

# PACK_NUM_FRONTEND = 3
LOCAL_ADDR = "192.168.30.10"
LOCAL_PORT = 15000
BUFF_SIZE = 1024
BYTE_ARRAY_SIZE = 42
HEADER_SIZE = 14
CRC_SIZE = 10
PAYLOAD_SIZE = BUFF_SIZE - BYTE_ARRAY_SIZE - HEADER_SIZE

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.bind((LOCAL_ADDR, LOCAL_PORT))
logging.info(f"Socket created and binded")


def receive_file(filename, filesize):
    with open(filename, 'wb') as f:
        packet_num = 1000
        while filesize > 0:
            data, addr_con = my_socket.recvfrom(BUFF_SIZE)
            f.write(data)
            filesize -= PAYLOAD_SIZE
            packet_num += 1
            my_socket.sendto(data, addr_con)


def stop_wait_sync(my_socket):
    ack_sent = False
    payload_real = b""
    set_crc = set()
    crc_1 = 0
    sender_pack_num = 0
    filesize = 0
    index = 3
    filename = ""

    while True:
        try:
            raw_data, addr_con = my_socket.recvfrom(BUFF_SIZE)
            header = raw_data[:HEADER_SIZE]
            payload = raw_data[HEADER_SIZE:]

            sender_pack_num = int((header[CRC_SIZE:]).decode())
            current_crc = crc32(payload)

            if int((header[:CRC_SIZE]).decode()) == current_crc:
                if sender_pack_num == 3 and index == 3:
                    logging.info(f"{payload}, {addr_con}")
                    index -= 1
                    filename = payload
                elif sender_pack_num == 2 and index == 2:
                    logging.info(f"{payload}, {addr_con}")
                    filesize = payload
                    index -= 1
                elif sender_pack_num == 1 and index == 1:
                    logging.info(f"{payload}, {addr_con}")
                    index -= 1
                elif sender_pack_num == 0:
                    return filename, filesize
        except:
            continue
        my_socket.sendto(str(index + 1).encode(), DEST_ADDR)


def stop_and_wait_receive(my_socket, filename, filesize):
    packet_num = 0
    last_crc = -1
    header = b""
    sender_pack_num = 0
    payload = b""
    current_crc = 0

    with open(filename, 'wb') as f:
        while filesize > 0:
            try:
                raw_data, addr = my_socket.recvfrom(BUFF_SIZE)
                header = raw_data[:HEADER_SIZE]
                payload = raw_data[HEADER_SIZE:]
                print(int((header[CRC_SIZE:]).decode()), packet_num, crc32(
                    payload), int((header[:CRC_SIZE]).decode()), crc32(
                    payload) == int((header[:CRC_SIZE]).decode()))
                sender_pack_num = int((header[CRC_SIZE:]).decode())
                current_crc = crc32(payload)

                if int((header[:CRC_SIZE]).decode()) == current_crc:
                    if packet_num == sender_pack_num and last_crc != current_crc:
                        f.write(payload)
                        packet_num += 1
                        filesize -= PAYLOAD_SIZE
                        last_crc = current_crc
                    my_socket.sendto(
                        str(int(packet_num - 1)).encode(), DEST_ADDR)
            except:
                continue

    while True:
        try:
            raw_data, addr = my_socket.recvfrom(BUFF_SIZE)
            header = raw_data[:HEADER_SIZE]
            if int(header[CRC_SIZE:].decode()) == (packet_num - 1):
                my_socket.sendto(
                    str(packet_num - 1).encode(), DEST_ADDR)
            else:
                break
        except:
            continue

    return md5_hash(filename)


if __name__ == '__main__':

    filename, filesize = stop_wait_sync(my_socket)

    file_hash = stop_and_wait_receive(
        my_socket, filename, int(filesize.decode("utf-8")))

    my_hashfile = md5_hash(filename)

    sender_hashfile, addr_con = my_socket.recvfrom(1024)

    while True:
        try:
            header = sender_hashfile[:HEADER_SIZE]
            payload = sender_hashfile[HEADER_SIZE:]
            crc = int(sender_hashfile[:CRC_SIZE].decode())
            while crc != int(crc32(payload)):
                sender_hashfile, addr_con = my_socket.recvfrom(1024)
                payload = sender_hashfile[HEADER_SIZE:]
                crc = int(sender_hashfile[:CRC_SIZE].decode())

            sender_hash = (payload.strip()).decode()
            break

        except:
            continue

    print(sender_hash)
    print(my_hashfile)

    NOT_OK = True
    while NOT_OK and (sender_hash != str(my_hashfile)):
        try:
            print(sender_hash)
            print(my_hashfile)

            if sender_hash != str(my_hashfile):
                while NOT_OK:
                    my_socket.settimeout(10)
                    while True:
                        try:
                            my_socket.sendto(b"NOTOK", DEST_ADDR)
                            my_socket.recvfrom(1024)
                            break
                        except:
                            continue

                    file_hash = stop_and_wait_receive(
                        my_socket, filename, int(filesize.decode("utf-8")))
                    my_hashfile = md5_hash(filename)
                    sender_hash, addr_con = my_socket.recvfrom(1024)
                    sender_hash == (sender_hash[HEADER_SIZE:]).decode()
                    if my_hashfile == sender_hash:
                        NOT_OK = False
                        break
            else:
                NOT_OK = False
                break

        except:
            continue

    if my_hashfile == sender_hash:
        my_socket.settimeout(5)
        while True:
            try:
                print("HERE")
                my_socket.sendto(b"OK", DEST_ADDR)
                ACK, addr_con = my_socket.recvfrom(1024)
                if ACK == b"OK":
                    NOT_OK = False
                    break
            except:
                continue

    logging.info(f"filesize from os.stat is {os.stat(filename).st_size}")

    my_socket.settimeout(2)
    while True:
        try:
            stop, addr = my_socket.recvfrom(1024)
            my_socket.sendto(b"0", DEST_ADDR)
        except socket.timeout:
            break
    print("end")
    my_socket.close()
