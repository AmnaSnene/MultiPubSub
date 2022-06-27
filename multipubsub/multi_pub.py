import threading
from datetime import datetime
from time import sleep
import time

from multipubsub.multi_pub_sub import PubSub

from paho.mqtt import client as mqtt_client


class Pub(PubSub):

    def publish(self, client: mqtt_client, client_id: str, topic: str) -> object:
        """
        This method allows the client to publisher the current timestamp each second to the self.topics (one topic).
        """
        msg_count = 0
        while True:
            msg = int(time.time())
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"{client_id} Send `{msg}` to topic `{topic}`")
            else:
                print(f"{client_id} Failed to send message to topic {topic}")
            msg_count += 1
            sleep(1)
            if msg_count == self.duration_to_disconnect:
                self.disconnect_mqtt(client, client_id)
                break

    def run(self, client_id: str):
        client = self.connect_mqtt(client_id)

        try:
            threads = list()
            for topic in self.topics:
                x = threading.Thread(target=self.publish, args=(client, client_id, topic))
                threads.append(x)
                x.start()

            for thread in threads:
                thread.join()

        except Exception as exception:
            print(exception)

