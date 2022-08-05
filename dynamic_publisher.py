import random

from multipubsub.multi_pub import Pub

publisher = Pub(host="pi3-r1-m1-l1-p1.pi3lan.local")

nb_pub = [2, 2, 2, 2, 20, 20, 20, 20, 2, 2, 2, 2, 20, 20, 20, 20]
nb_topic = [2, 10, 2, 10, 2, 2, 10, 10, 2, 10, 2, 10, 10, 10, 2, 2]
while True:
    for i in range(16):
        publisher.topics_nb = nb_topic[i]
        publisher.client_nb = nb_pub[i]
        publisher.msg_per_second = random.randint(2, 200)
        publisher.msg_size = random.randint(16, 200)
        publisher.publishing_duration = 10
        publisher.run_multiple()
