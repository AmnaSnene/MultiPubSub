import _thread
import time
from time import sleep

from paho.mqtt import client as mqtt_client


class PubSub:
    """
    host is the hostname or IP address of the remote broker. Defaults to localhost.
    port is the network port of the server host to connect to. Defaults to 1883.
    sub_nb is the number of subscribers. Defaults to 1.
    """

    def __init__(self, host="localhost", port=1883, client_nb=1):
        self._host = host
        self._port = port
        self._client_nb = client_nb
        self._topics = None
        self._qos = 0
        self._duration_to_unsubscribe = 0
        self._duration_to_disconnect = 0

    @property
    def topics(self):
        return self._topics

    @topics.setter
    def topics(self, topics: list) -> None:
        self._topics = topics

    @property
    def qos(self):
        return self._qos

    @qos.setter
    def qos(self, qos: int) -> None:
        self._qos = qos

    @property
    def duration_to_unsubscribe(self):
        return self._duration_to_unsubscribe

    @duration_to_unsubscribe.setter
    def duration_to_unsubscribe(self, duration_to_unsubscribe: int) -> None:
        self._duration_to_unsubscribe = duration_to_unsubscribe

    @property
    def duration_to_disconnect(self):
        return self._duration_to_disconnect

    @duration_to_disconnect.setter
    def duration_to_disconnect(self, duration_to_disconnect: int) -> None:
        self._duration_to_disconnect = duration_to_disconnect

    def connect_mqtt(self, client_id: int) -> mqtt_client:
        """
        :param client_id:
        :return:
        """

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"Client {client_id} Connected to MQTT Broker!")
            else:
                print(f"Client {client_id} Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client('sub-{}'.format(client_id))
        client.on_connect = on_connect
        client.connect(self._host, self._port)
        return client



    def disconnect_mqtt(self, client: mqtt_client, client_id: int):
        def on_disconnect(client, userdata, rc):
            if rc != 0:
                print(f"Client {client_id} Unexpected disconnection.")
            else:
                print(f"Client {client_id} Disconnected!")

        mqtt_client.on_disconnect = on_disconnect
        client.disconnect()

    def subscribe(self, client: mqtt_client, client_id: int):
        def on_message(client, userdata, msg):
            print(f"Client{client_id} Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        subscription_list = [(topic, self.qos) for topic in self.topics]
        client.subscribe(subscription_list)
        client.on_message = on_message

    def unsubscribe(self, client: mqtt_client, client_id):
        def on_unsubscribe(client, userdata, mid):
            print("unsubscribed from {}".format(self.topics))

        client.on_unsubscribe = on_unsubscribe
        client.unsubscribe(self.topics)

    def publish(self, client: mqtt_client, client_id: int):
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

    def run(self, client_id: int, sub_or_sub: str):
        client = self.connect_mqtt(client_id)
        if sub_or_sub == 'sub':
            self.subscribe(client, client_id)
        else:
            self.publish(client, client_id)
        client.loop_start()
        if self.duration_to_unsubscribe:
            sleep(self.duration_to_unsubscribe)
            self.unsubscribe(client, client_id)
        if self.duration_to_disconnect:
            sleep(self.duration_to_disconnect)
            self.disconnect_mqtt(client, client_id)
            client.loop_stop()

    def run_multiple(self, first_client_id=1, pub_or_sub="sub"):
        try:
            for i in range(first_client_id, first_client_id + self._client_nb):
                _thread.start_new_thread(self.run, (i, pub_or_sub))
        except Exception as exception:
            print(exception)
        while 1:
            pass