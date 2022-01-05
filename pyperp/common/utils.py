import time


def getDeadline(expiry_seconds: int):
    return int(time.time()) + expiry_seconds
