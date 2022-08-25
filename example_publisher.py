
# create Pub object with 1 client to run later.
from multipubsub.multi_pub import Pub

publishers = Pub(port=1883, client_nb=1, topics_nb=1, host="localhost")
publishers.msg_per_second = 1
publishers.run_multiple()
# specify the topics to publish on.
#publishers.topics = ['topic/']

# disconnect after 40 seconds

#publishers.duration_to_disconnect = 40


# run client: publisher.

