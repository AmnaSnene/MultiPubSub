from multipubsub.multi_pub_sub import PubSub

subscribers = PubSub(client_nb=4)
subscribers.topics = ['PUBLISH TO 1883 BROKER/']
# subscribers.duration_to_unsubscribe = 30

subscribers.run_multiple(6, pub_or_sub="pub")

subscribers.run_multiple()
