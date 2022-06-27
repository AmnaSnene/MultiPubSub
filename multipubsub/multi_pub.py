from time import sleep
import time

from multipubsub.multi_pub_sub import PubSub

from paho.mqtt import client as mqtt_client


class Pub(PubSub):

    def publish(self, client: mqtt_client, client_id: int):
        """
        This method allows the client to publisher the current timestamp each second to the self.topics (one topic).
        """
        msg_count = 0
        while True:
            msg = int(time.time())
            result = client.publish(self.topics[0], msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Client {client_id} Send `{msg}` to topic `{self.topics}`")
            else:
                print(f"Client {client_id} Failed to send message to topic {self.topics}")
            msg_count += 1
            sleep(1)
            if msg_count == self.duration_to_disconnect:
                self.disconnect_mqtt(client, client_id)
                break

    def run(self, client_id: int):
        client = self.connect_mqtt(client_id)
        self.publish(client, client_id)