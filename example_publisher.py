from multipubsub.multi_pub_sub import PubSub

# create PubSub object with 5 client to run later.
publishers = PubSub(client_nb=5)
# specify the topics to publish on.
publishers.topics = ['topic/']

# disconnect after 40 seconds
# publishers.duration_to_disconnect = 40

# run clients: publishers.
# the first publisher id  is client_1 ... the final publisher id is client_5 .
publishers.run_multiple(pub_or_sub="pub")
