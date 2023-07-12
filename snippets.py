import hashlib


import hashlib


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def file_as_bytes(file):
    with file:
        return file.read()


if __name__ == "__main__":
    result = md5("Gotcha.jpg")
    print(type(result))
    print(hashlib.md5(file_as_bytes(open("Gotcha.jpg", 'rb'))).hexdigest())

    # f = open("Gotcha.jpg", "rb")
    # def what(): yield f.read(10)
    # print(next(what()))
    # f.close()
