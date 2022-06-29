from multipubsub.multi_pub import Pub

# create Pub object with 1 client to run later.
publishers = Pub(port=1883, client_nb=1, topics_nb=2)
# specify the topics to publish on.
#publishers.topics = ['topic/']

# disconnect after 40 seconds

publishers.duration_to_disconnect = 40


# run client: publisher.
publishers.run_multiple()
