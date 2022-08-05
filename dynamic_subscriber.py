from multipubsub.multi_sub import Sub

subscribers = Sub(host="pi3-r1-m1-l1-p1.pi3lan.local")

nb_sub = [2, 2, 20, 20, 20, 20, 20, 20, 2, 2, 20, 20, 2, 2, 2, 2]
nb_topic = [2, 2, 2, 10, 10, 2, 2, 10, 10, 10, 10, 2, 2, 10, 2, 10]
while True:
    for i in range(16):
        subscribers.client_nb = nb_sub[i]
        subscribers.topics_nb = nb_topic[i]
        subscribers.duration_to_disconnect = 10
        subscribers.run_multiple()
