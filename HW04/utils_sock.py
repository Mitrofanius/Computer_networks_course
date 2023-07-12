from zlib import crc32
from hashlib import md5
CRC_SIZE = 10

INDEX_SIZE = 4


def crc_format(crc):
    missing_places = CRC_SIZE - len(str(crc))
    return b'0' * missing_places + str(crc).encode("utf-8")


# def udp_format(data):
#     if (isinstance(data, bytes)):
#         crc = crc32(data)
#         return crc_format(crc) + data
#     else:
#         crc = crc32(str(data).encode("utf-8"))
#         return crc_format(crc) + str(data).encode("utf-8")


def index_format(index):
    missing_places = INDEX_SIZE - len(str(index))
    return b'0' * missing_places + str(index).encode("utf-8")


def udp_format(data, index):
    if (isinstance(data, bytes)):
        crc = crc32(data)
        return crc_format(crc) + index_format(index) + data
    else:
        crc = crc32(str(data).encode("utf-8"))
        return crc_format(crc) + index_format(index) + str(data).encode("utf-8")

# Returns index format INDEX_SIZE digits


def md5_format(filename):
    hash_md5 = md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest().encode("utf-8")


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
