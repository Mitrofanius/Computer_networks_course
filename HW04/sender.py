import socket
import os
from zlib import crc32
from hashlib import md5
from utils_sock import md5_format, udp_format, Colors
from time import sleep

# socket info
TARGET_IP = "192.168.30.19"
# TARGET_IP = "127.0.0.1"
TARGET_PORT = 14001

DESTINATION_ADDRESS = (TARGET_IP, TARGET_PORT)

# LOCAL_IP = "127.0.0.1"
LOCAL_IP = "192.168.30.10"
LOCAL_PORT = 15000

LOCAL_ADDRESS = (LOCAL_IP, LOCAL_PORT)
# ------------------------------------


# Useless Bohdan's headers
WINDOW_SIZE = 100
BUFF_SIZE = 1024
CRC_SIZE = 10
INDEX_SIZE = 4
BYTE_ARRAY_SIZE = 33
UPD_HEADER_SIZE = 9
HEADER_SIZE = CRC_SIZE + INDEX_SIZE
PAYLOAD_SIZE = BUFF_SIZE - HEADER_SIZE - \
    BYTE_ARRAY_SIZE - UPD_HEADER_SIZE  # 968
# ------------------------------------------------------------------------------


def receive_hash(my_socket):
    cnt = 0
    ret = "RESEND"
    while True:
        if cnt >= 30:
            return ret
        try:
            msg, addr = my_socket.recvfrom(BUFF_SIZE)
            print(f"msg = {msg}")
            msg = msg[HEADER_SIZE:]
            if msg == b"OKAY":
                send_stop_and_wait(my_socket, b"ACK")
                ret = "OK"
                return ret
            elif msg == b"RESEND":
                send_stop_and_wait(my_socket, b"ACK")
                return ret
            else:
                cnt += 1
        except socket.timeout:
            cnt += 1
            continue
        except ValueError:
            continue


def send_stop_and_wait(my_socket, message):
    acknowledged = False
    cnt = 0
    err_cnt_2 = 0

    while not acknowledged:
        my_socket.sendto(udp_format(message, -1), DESTINATION_ADDRESS)
        sleep(0.3)

        try:
            ACK, address = my_socket.recvfrom(BUFF_SIZE)
            if len(ACK) >= HEADER_SIZE:
                print(ACK)
                msg = ACK
                print(f"msg = {msg}")
                msg = msg[HEADER_SIZE:]
                if msg == b"OKAY" or msg == b"RESEND" or len(msg) == HEADER_SIZE:
                    return "OKAY"

            if ACK == b"ACK":
                acknowledged = True
                print(
                    f"||{Colors.OKGREEN}Acknowledgment has been successfully received.{Colors.ENDC}")
                return "ACK"
            else:
                print(
                    f"||{Colors.FAIL}Acknowledge ACK is wrong. Sending again...{Colors.ENDC}")
        except socket.timeout:
            cnt += 1
            if cnt == 10:
                print("Wait for frames for too long")
                return "timed out"
            continue


def retransmit(my_socket, buffer, last_acknowledged):
    print("In retransmit")
    data = buffer[0][1]
    my_socket.sendto(udp_format(data, last_acknowledged + 1),
                     DESTINATION_ADDRESS)


def update_buffer(buffer, last_ack):
    to_delete = []
    print("updating buffer")
    print(buffer[0][0])

    for i in range(len(buffer)):
        if buffer[i][0] <= last_ack:
            to_delete.append(i)

    cnt = 0
    for i in to_delete:
        buffer.pop(i - cnt)
        cnt += 1

    print("updated buffer down there")
    if len(buffer) > 0:
        print(buffer[0][0])

    # return buffer


def receive_acks(my_socket, buffer, last_acknowledged, buffer2):
    print("in recieve acks")
    cnt = 0
    while True:
        print("in recieve acks while")

        try:
            msg, addr = my_socket.recvfrom(1024)
            if msg == b"NAK":
                return "stop"

            if len(msg) <= HEADER_SIZE:
                continue

            rec_index = int((msg[HEADER_SIZE:]).decode())

            if last_acknowledged < rec_index < last_acknowledged + WINDOW_SIZE:
                last_acknowledged = rec_index

            elif last_acknowledged - WINDOW_SIZE < rec_index < last_acknowledged and last_acknowledged >= 0:
                buffer = buffer2.copy()
                last_acknowledged = rec_index

                # elif last_acknowledged >= 0:
                #     cnt += 1
                #     if cnt >= 1:
                #         cnt = 0
                #         return str(rec_index)

        except socket.timeout:
            return last_acknowledged

        except ValueError:
            continue


def send_file_selective_repeat(my_socket, filename, filesize):
    hash_md5 = md5()

    file = open(filename, "rb")
    buffer = []
    buffer2 = []
    not_sent = True
    last_acknowledged = -1
    index = 0
    num_packs = int(filesize // PAYLOAD_SIZE +
                    (1 if filesize % PAYLOAD_SIZE != 0 else 0)) - 1

    print("Before first while")
    print("")

    while last_acknowledged < num_packs:
        while index < last_acknowledged + WINDOW_SIZE:
            print("Befor first while")
            print(f"sending packet {index}")
            print()

            data = file.read(PAYLOAD_SIZE)
            buffer.append((index, data))
            buffer2.append((index, data))
            my_socket.sendto(udp_format(data, index), DESTINATION_ADDRESS)
            index += 1

        last_acknowledged = receive_acks(
            my_socket, buffer, last_acknowledged, buffer2)
        if last_acknowledged == 'stop':
            file.close()
            return
        # elif isinstance(last_acknowledged, str):
        #     last_acknowledged = int(last_acknowledged)
        #     file.seek(PAYLOAD_SIZE * int(last_acknowledged))
        print(f"last acknowledged = {last_acknowledged}")
        update_buffer(buffer, last_acknowledged)

        if len(buffer2) >= 2 * WINDOW_SIZE:
            buffer2 = buffer.copy()

        if index >= last_acknowledged + WINDOW_SIZE:
            print("In if")
            print()
            retransmit(my_socket, buffer, last_acknowledged)

    file.close()


if __name__ == "__main__":
    filename = "Andy.jpg"
    filesize = os.stat(filename).st_size

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("shit")
    my_socket.bind(LOCAL_ADDRESS)
    my_socket.settimeout(1)

    # while True:
    #     my_socket.sendto(b"HEYYEYefghewgveoiEYDYE", DESTINATION_ADDRESS)
    #     sleep(0.25)

    send_stop_and_wait(my_socket, filename)
    send_stop_and_wait(my_socket, filesize)
    send_stop_and_wait(my_socket, "START")

    binary_hash = md5_format(filename)
    while True:
        send_file_selective_repeat(my_socket, filename, filesize)
        ret = send_stop_and_wait(my_socket, binary_hash)
        print(ret, "this return")
        if ret == "ACK":
            if receive_hash(my_socket) == "OK":
                break
            else:
                pass
        elif ret == "OKAY":
            send_stop_and_wait(my_socket, "ACK")
            break

    send_stop_and_wait(my_socket, "STOP")

    my_socket.close()
