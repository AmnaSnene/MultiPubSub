from multipubsub.multi_pub_sub import PubSub

# create PubSub object with 4 client to run later.
subscribers = PubSub(client_nb=4, port=1883, host='localhost')
# specify the topics to subscribe to.
subscribers.topics = ['PUBLISH TO 1883 BROKER/', 'topic/']
# unsubscribe after 30 seconds
subscribers.duration_to_unsubscribe = 30
# disconnect after 10 seconds
subscribers.duration_to_disconnect = 10

# run clients: subscribers.
# the first subscriber id  is client_6, the second is client_7, the third is client_8 and the fourth is client_9.
subscribers.run_multiple(6, pub_or_sub="sub")
