from datetime import datetime


def get_client_id():
    dt = datetime.now()
    # getting the timestamp
    ts = int(datetime.timestamp(dt) * 10 ** 6)
    return f"Client{ts}"


def get_new_topic(new_topics_nb):
    new_topics = []
    for i in range(new_topics_nb):
        dt = datetime.now()
        # getting the timestamp
        ts = int(datetime.timestamp(dt) * 10 ** 5)
        new_topics.append(f"topic{ts}")
    return new_topics
