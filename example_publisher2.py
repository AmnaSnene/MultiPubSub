from time import sleep

from multipubsub.multi_pub_sub import PubSub

from paho.mqtt import client as mqtt_client


# override publish method to customize the publisher behavior.
class Pub(PubSub):
    def publish(self, client: mqtt_client, client_id: int):
        msg_count = 0
        while True:
            result = client.publish(self.topics[0], msg_count)
            status = result[0]
            if status == 0:
                print(f"Client {client_id} Send `{msg_count}` to topic `{self.topics}`")
            else:
                print(f"Client {client_id} Failed to send message to topic {self.topics}")
            msg_count += 1
            sleep(3)


publisher = Pub()
publisher.topics = ["topic/"]
publisher.run_multiple(pub_or_sub="pub")
