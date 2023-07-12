# import socket
# import os
# from zlib import crc32
# from hashlib import md5


# class Colors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKCYAN = '\033[96m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'


# TARGET_IP = "127.0.0.1"
# TARGET_PORT = 14000

# DESTINATION_ADDRESS = (TARGET_IP, TARGET_PORT)

# #LOCAL_IP = "192.168.30.33"
# LOCAL_IP = "127.0.0.1"
# LOCAL_PORT = 15001

# LOCAL_ADDRESS = (LOCAL_IP, LOCAL_PORT)

# FOLDER_PATH = "C:\\Users\\Bablos\\Desktop\\"
# FILE_NAME = "Andy.jpg"
# FILE_PATH = FOLDER_PATH + FILE_NAME
# FILE_SIZE = os.stat(FILE_PATH).st_size

# BUFF_SIZE = 1024
# CRC_SIZE = 10
# INDEX_SIZE = 4
# BYTE_ARRAY_SIZE = 33
# UPD_HEADER_SIZE = 9
# HEADER_SIZE = CRC_SIZE + INDEX_SIZE
# PAYLOAD_SIZE = BUFF_SIZE - HEADER_SIZE - \
#     BYTE_ARRAY_SIZE - UPD_HEADER_SIZE  # 968

# SOCKET_TIMEOUT = 0.25

# PRINT_MODULO = 1

# START = "START"
# STOP = "STOP"
# OK = "OK"
# PACKET = "PACKET"
# HASH = "HASH MD5"
# global RESENT
# NOTOK = "NOTOK"


# def stop_and_wait(program_socket, name, index, data, destination_address):
#     acknowledged = False
#     global RESENT

#     # spam destination_address until it acknowledge me
#     while (not acknowledged):
#         program_socket.sendto(upd_format(index, data), destination_address)

#         try:
#             if (index % PRINT_MODULO == 0):
#                 print(
#                     f"            ||{Colors.WARNING}Trying to get ACK...{Colors.ENDC}")
#             ACK, address = program_socket.recvfrom(BUFF_SIZE)

#             if (ACK == str(index).encode()):
#                 if (index % PRINT_MODULO == 0):
#                     print(
#                         f"            ||{Colors.OKGREEN}Acknowledgment has been successfully received.{Colors.ENDC}")
#                 acknowledged = True
#             elif (ACK == OK.encode()):
#                 if (index % PRINT_MODULO == 0):
#                     print(f"            ||{Colors.OKCYAN}{OK}{Colors.ENDC}")
#                     print(
#                         f"        []{Colors.OKGREEN}The file has NOT been damaged.\n{Colors.ENDC}")
#                 program_socket.sendto(b'OK', destination_address)
#                 RESENT = False
#                 acknowledged = True
#             elif (ACK == NOTOK.encode()):
#                 if (index % PRINT_MODULO == 0):
#                     print(f"            ||{Colors.OKCYAN}{NOTOK}{Colors.ENDC}")
#                     print(
#                         f"        []{Colors.FAIL}The file has been damaged. Stating the sending process again...{Colors.ENDC}\n")
#                 RESENT = True
#                 acknowledged = True
#             else:
#                 if (index % PRINT_MODULO == 0):
#                     print(
#                         f"            ||{Colors.FAIL}Acknowledge index or ACK is wrong. Sending again...{Colors.ENDC}")
#         except socket.timeout:
#             if(name == "PACKET"):
#                 print(
#                     f"            ||{Colors.FAIL}Time is over. The {name} [#{index}] has not been sent.{Colors.ENDC}")
#             else:
#                 print(
#                     f"            ||{Colors.FAIL}Time is over. The {name} has not been sent.{Colors.ENDC}")

# # Returns upd format


# def upd_format(index, data):
#     if (isinstance(data, bytes)):
#         crc = crc32(data)
#         return crc_format(crc) + index_format(index) + data
#     else:
#         crc = crc32(str(data).encode("utf-8"))
#         return crc_format(crc) + index_format(index) + str(data).encode("utf-8")

# # Returns index format INDEX_SIZE digits


# def index_format(index):
#     missing_places = INDEX_SIZE - len(str(index))
#     return b'0' * missing_places + str(index).encode("utf-8")

# # Returns crc format CRC_SIZE digits


# def crc_format(crc):
#     missing_places = CRC_SIZE - len(str(crc))
#     return b'0' * missing_places + str(crc).encode("utf-8")

# # Sends the name of the file to the listener


# def send_file_name(program_socket, index):
#     print(f"    []{Colors.WARNING}Sending the name of the file...{Colors.ENDC}")
#     print(
#         f"    ||{Colors.OKBLUE}The name of the file is [{FILE_NAME}] in [{FOLDER_PATH}]{Colors.ENDC}")
#     stop_and_wait(program_socket, FILE_NAME, index,
#                   FILE_NAME, DESTINATION_ADDRESS)
#     print(
#         f"    []{Colors.OKGREEN}The file name has been sccessfully sent.{Colors.ENDC}\n")

# # Sends the size of the file in bytes to the listener


# def send_file_size(program_socket, index):
#     print(f"    []{Colors.WARNING}Sending the size of the file...{Colors.ENDC}")
#     print(
#         f"    ||{Colors.OKBLUE}The size of the file is [{FILE_SIZE}] bytes.{Colors.ENDC}")
#     stop_and_wait(program_socket, FILE_SIZE, index,
#                   FILE_SIZE, DESTINATION_ADDRESS)
#     print(
#         f"    []{Colors.OKGREEN}The size of the file has been successfully sent.{Colors.ENDC}\n")

# # Sends START keyword


# def send_keyword(program_socket, keyword, index):
#     print(f"    []{Colors.WARNING}Sending the {keyword} keyword...{Colors.ENDC}")
#     stop_and_wait(program_socket, keyword, index, keyword, DESTINATION_ADDRESS)
#     print(
#         f"    []{Colors.OKGREEN}The keyword {keyword} has been successfully sent.{Colors.ENDC}\n")


# def md5_format():
#     hash_md5 = md5()
#     with open(FILE_PATH, "rb") as f:
#         for chunk in iter(lambda: f.read(4096), b""):
#             hash_md5.update(chunk)
#     return hash_md5.hexdigest().encode("utf-8")

# # Sends the file in loop piece by piece, BUFFERS_LEN each time


# def send_file(program_socket):
#     print(f"    []{Colors.WARNING}Trying to open the file...{Colors.ENDC}")
#     with open(FILE_PATH, "rb") as file:
#         print(
#             f"    ||{Colors.OKGREEN}The file has been successfully opened.{Colors.ENDC}\n")
#         notSent = True
#         sizeTMP = FILE_SIZE
#         index = 0

#         print(
#             f"        []{Colors.WARNING}Staring the sending process...{Colors.ENDC}\n")
#         while (notSent):
#             if (index % PRINT_MODULO == 0):
#                 print(
#                     f"        ||{Colors.WARNING}Sending the [#{index}] packet...{Colors.ENDC}")
#             # Reads and sends data
#             stop_and_wait(program_socket, PACKET, index,
#                           file.read(PAYLOAD_SIZE), DESTINATION_ADDRESS)
#             if (index % PRINT_MODULO == 0):
#                 print(
#                     f"        ||{Colors.OKGREEN}The [#{index}] packet has been successfully sent.{Colors.ENDC}\n")

#             sizeTMP -= PAYLOAD_SIZE

#             if (sizeTMP <= 0):
#                 notSent = False

#             index += 1

#         print(
#             f"        []{Colors.OKGREEN}The sending process has been successfully ended.{Colors.ENDC}\n")
#     print(
#         f"    ||{Colors.OKBLUE}[{FILE_SIZE}] bytes has been sent.{Colors.ENDC}")
#     print(
#         f"    []{Colors.OKGREEN}The file has been successfully closed.{Colors.ENDC}\n")


# if __name__ == "__main__":

#     # START of the program
#     print(f"[]{Colors.OKCYAN}START.{Colors.ENDC}\n")

#     # Creates a new socket
#     socket.setdefaulttimeout(SOCKET_TIMEOUT)
#     print(f"    []{Colors.WARNING}Trying to create a new socket...{Colors.ENDC}")
#     program_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     program_socket.bind(LOCAL_ADDRESS)
#     print(
#         f"    []{Colors.OKGREEN}The socket has been successfully created.{Colors.ENDC}\n")

#     # Sends the name of the file to the listener
#     send_file_name(program_socket, 3)

#     # Sends the size of the file in bytes to the listener
#     send_file_size(program_socket, 2)

#     # Sends START keyword
#     send_keyword(program_socket, START, 1)

#     # Sends the file until the hash is the same
#     while (True):
#         # Sends the file in loop piece by piece, BUFFERS_LEN each time
#         send_file(program_socket)

#         # Checks the hash of the file
#         print(f"        []{Colors.OKGREEN}Checking md5...{Colors.ENDC}")
#         stop_and_wait(program_socket, HASH, 0,
#                       md5_format(), DESTINATION_ADDRESS)

#         if (not RESENT):
#             break

#     # Sends STOP keyword
#     send_keyword(program_socket, STOP, 0)

#     # END of the program
#     program_socket.close()
#     print(
#         f"    []{Colors.OKGREEN}The socket has been successfully closed.{Colors.ENDC}\n")
#     print(f"[]{Colors.OKCYAN}End.{Colors.ENDC}")
