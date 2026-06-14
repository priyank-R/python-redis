def readCommand(data: bytes) -> tuple[object, int, Exception | None]:
    pass


def readSimpleString(data: bytes) -> tuple[str, int, Exception | None]:
    pos = 1
    while data[pos] != ord("\r"):
        pos = pos + 1

    return data[1:pos].decode('utf-8'), pos + 2, None


def readError(data: bytes) -> tuple[str, int, Exception | None]:
    return readSimpleString(data)


def readBulkString(data: bytes) -> tuple[str, int, Exception | None]:
    """ '$6\r\nyellow\r\n' """
    pos = 1
    length, delta, error = readLength(data[pos:])
    pos = pos + delta

    return data[pos:(pos+length)].decode('utf-8'), pos + length + 2, None


def readLength(data: bytes) -> tuple[int, int, Exception | None]:
    pos  = 0

    while data[pos] >= ord('0') and data[pos] <= ord('9'):
        pos+=1

    len = int(data[0:pos].decode('utf-8'))

    return len, pos + 2, None

def readArray(data: bytes) -> tuple[str, int, Exception | None]:
    """ 
        Eg. *3\r\n$3\r\nhey\r\n$3\r\nmey\r\n$3\r\nnay\r\n\r\n
        Represents ['hey','mey','nay']

    """
    pos = 1
    arr = []

    length, delta, e = readLength(data[pos:])
    pos+= delta

    for i in range(0, length):
        v, d, e = decodeOne(data[(pos): ])
        arr.append(v)
        pos+= d
    
    return arr, pos, None


def readInt64(data: bytes) -> tuple[int, int, Exception | None]:
    value, delta, error = readSimpleString(data)
    if value:
        return int(value), delta, None
    return None, 0, error




def decodeOne(data: bytes) -> tuple[object, int, Exception | None]:
    if len(data) == 0:
        return None, 0, Exception("No data")

    if data[0] == ord("+"):
        return readSimpleString(data)

    if data[0] == ord("-"):
        return readError(data)

    if data[0] == ord(":"):
        return readInt64(data)

    if data[0] == ord("$"):
        return readBulkString(data)

    if data[0] == ord("*"):
        return readArray(data)

    return None, 0, None


def decode(data: bytes) -> tuple(object, Exception | None):
    if len(data) == 0:
        return None, Exception("No data")

    value, _, error = decodeOne()
    return value, error
