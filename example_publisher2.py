from multipubsub.multi_pub import Pub

# 20 pubs, 2 Topics, multiply *2 nb_msg_per_second each 4 second until nb_msg_per_second = 1024
publisher = Pub(client_nb=20, topics_nb=2)

for i in range(11):
    publisher.publishing_duration = 4
    publisher.run_multiple()
    publisher.msg_per_second *= 2
