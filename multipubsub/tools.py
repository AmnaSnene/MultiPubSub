import struct
import time
import uuid
from datetime import datetime


def get_client_id():
    dt = datetime.now()
    # getting the timestamp
    ts = int(datetime.timestamp(dt) * 10 ** 6)
    return f"Client{ts}"


def get_t_end_publishing(duration_to_disconnect, publishing_duration):
    try:
        # get the min of duration_to_disconnect and publishing_duration if they exist. Defaults to None.
        duration = min([i for i in [duration_to_disconnect, publishing_duration] if i]) + 1
    except:
        # 7 July 2322
        duration = 11124244037

    return duration


def calculate_latency(data, client):
    latency = time.time_ns() - data[0]
    if data[1] == uuid.getnode():
        client.publish("latency", struct.pack('ll', latency, uuid.getnode()))


def create_msg(size):
    pad_byte = size - 16
    return struct.pack('ll{}'.format('x' * pad_byte), time.time_ns(), uuid.getnode())


def unpack_msg(msg):
    return struct.unpack_from('ll', msg)
