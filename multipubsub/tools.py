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
