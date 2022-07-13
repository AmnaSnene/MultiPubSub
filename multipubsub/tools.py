import os
import sys
import time
from datetime import datetime
import uuid


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


def get_msg(size):
    return str(time.time_ns()) + ',' + str(uuid.getnode())


# Using os.urandom() method
a = os.urandom(2)

#print(asizeof.asizeof(a))
#print(sys.getsizeof(a))
