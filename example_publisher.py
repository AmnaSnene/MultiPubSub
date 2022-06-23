from multipubsub.multi_pub_sub import PubSub

# create PubSub object with 1 client to run later.
publishers = PubSub()
# specify the topics to publish on.
publishers.topics = ['topic/']

# disconnect after 40 seconds
publishers.duration_to_disconnect = 40


# run client: publisher.
publishers.run_multiple(pub_or_sub="pub")
