import random

from multipubsub.multi_pub import Pub

# Create multiple publishers client connected to one MQTT broker
# The number of clients, topics, msg per second and msg size change every 15s


publisher = Pub(port=1884, host="localhost")

nb_client = [1, 1, 1, 1, 10, 10, 10, 10, 1, 1, 1, 1, 10, 10, 10, 10]
nb_topic = [1, 5, 1, 5, 1, 1, 5, 5, 1, 5, 1, 5, 5, 5, 1, 1]
while True:
    for i in range(len(nb_client)):
        publisher.topics_nb = nb_topic[i]
        publisher.client_nb = nb_client[i]
        publisher.msg_per_second = random.randint(2, 10)
        publisher.msg_size = random.randint(16, 200)
        publisher.publishing_duration = 15
        publisher.run_multiple()
