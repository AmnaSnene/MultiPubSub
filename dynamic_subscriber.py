from multipubsub.multi_sub import Sub

# Create multiple subscribers clients subscribed to one MQTT broker
# In this example I adopted a dynamic scenario: the system state changes every 15s.

# Create Sub object with the broker address
subscribers = Sub(host="localhost", port=1883)


nb_client = [1, 1, 5, 5, 5, 5, 5, 5, 1, 1, 5, 5, 1, 1, 1, 1]
nb_topic = [1, 1, 1, 3, 3, 1, 1, 3, 3, 3, 3, 1, 1,3, 1, 3]

while True:
    for i in range(len(nb_client)):
        subscribers.client_nb = nb_client[i]
        subscribers.topics_nb = nb_topic[i]
        subscribers.duration_to_unsubscribe = 15
        subscribers.run_multiple()
