from multipubsub.multi_sub import Sub

# create Sub object with 4 client to run later.
subscribers = Sub(client_nb=4, port=1883, host='localhost', topics_nb=40)
# specify the topics to subscribe to.
subscribers.topics = ['PUBLISH TO 1883 BROKER/', 'topic/']
# unsubscribe after 30 seconds
subscribers.duration_to_unsubscribe = 30
# disconnect after 10 seconds
subscribers.duration_to_disconnect = 10

# run clients: subscribers.
subscribers.run_multiple()
