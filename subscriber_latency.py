import csv
import time
from datetime import datetime

from multipubsub import tools
from multipubsub.multi_sub import Sub
from paho.mqtt import client as mqtt_client

now = datetime.now()
current_time = now.strftime("%m%d%Y-%H:%M:%S")

# Open new file and write the header
file_name = f'latency-{current_time}.csv'
f = open(file_name, 'w')
header = ["latency", "sender_id", "time"]
writer = csv.writer(f)
writer.writerow(header)
f.close()


class SubLatency(Sub):
    def subscribe(self, client: mqtt_client):
        """
        This method subscribes the client to one or multiple topics.
        """

        def on_message(client, userdata, msg):
            """
            The callback function.
            """
            data = [i for i in tools.unpack_msg(msg.payload)]
            f1 = open(file_name, 'a')
            writer1 = csv.writer(f1)
            data.append(time.time_ns())
            writer1.writerow(data)
            f1.close()
            print(f"Latency {data} received from `{msg.topic}` topic")
            # print("recieved")

        def on_subscribe(client, userdata, mid, granted_qos):
            print(f"Subscribed{client._client_id.decode()}")

        client.on_subscribe = on_subscribe
        subscription_list = [(topic, self.qos) for topic in self.topics]
        client.subscribe(subscription_list)
        client.on_message = on_message


# create Sub object with 4 client to run later.
#subscribers = SubLatency(host="pi3-r1-m1-l1-p1.pi3lan.local")
subscribers = SubLatency(host="localhost")

subscribers.topics = ['latency']
subscribers.run_multiple()
