import datetime
from time import sleep

from multipubsub.multi_pub import Pub

from paho.mqtt import client as mqtt_client


# override publish method to customize the publisher behavior.
class CustomizedPub(Pub):
    def publish(self, client: mqtt_client, client_id: str, topic: str):
        dt = datetime.datetime.now()
        # getting the timestamp
        ts = int(datetime.datetime.timestamp(dt))
        msg_count = 0
        diff = 0
        while diff < 1:
            dt1 = datetime.datetime.now()
            # getting the timestamp
            ts1 = int(datetime.datetime.timestamp(dt1))
            result = client.publish(self.topics[0], msg_count)
            status = result[0]
            if status == 0:
                print(f"Client {client_id} Send `{msg_count}` to topic `{self.topics}`")
            else:
                print(f"Client {client_id} Failed to send message to topic {self.topics}")
            msg_count += 1
            diff = ts1 - ts
            if msg_count > 1000:
                break
            sleep(0.0002)
        print(msg_count)

publisher = CustomizedPub()
publisher.topics = ["topic/"]
publisher.run_multiple()
