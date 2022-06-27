import abc
import threading
from time import sleep
from abc import ABC
from paho.mqtt import client as mqtt_client


class PubSub(ABC):
    """
    This class allows to create multiple MQTT publishers or subscribers with the same behavior.
    This can be useful for benchmarking MQTT Broker performances.

    host is the hostname or IP address of the remote broker. Defaults to localhost.
    port is the network port of the server host to connect to. Defaults to 1883.
    client_nb is the number of clients (publishers or subscribers). Defaults to 1.
    """

    def __init__(self, host="localhost", port=1883, client_nb=1):
        self._host = host
        self._port = port
        self._client_nb = client_nb
        self._topics = None
        self._qos = 0
        self._duration_to_disconnect = 0

    """
    topics attribute type should be a list. If you are creating publishers, 
    you should provide the topic that the message should be published on as a list. 
    Example: ["mqtt/temp"] 
    It allows to subscribe to multiple topics at once.
    Example: ["mqtt/temp", "mqtt/level" ...]
    """

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

    """
    If you want to disconnect after n seconds, you should change the default value of the attribute
    duration_to_disconnect. Defaults to 0.
    """

    @property
    def duration_to_disconnect(self):
        return self._duration_to_disconnect

    @duration_to_disconnect.setter
    def duration_to_disconnect(self, duration_to_disconnect: int) -> None:
        self._duration_to_disconnect = duration_to_disconnect

    def connect_mqtt(self, client_id: int) -> mqtt_client:
        """
        This method connects the client to a broker.
        :param client_id:
        :return:
        """

        def on_connect(client, userdata, flags, rc):
            """
            The Callback function.
            """
            if rc == 0:
                print(f"Client {client_id} Connected to MQTT Broker!")
            else:
                print(f"Client {client_id} Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client('Client-{}'.format(client_id))
        client.on_connect = on_connect
        client.connect(self._host, self._port)
        return client

    def disconnect_mqtt(self, client: mqtt_client, client_id: int):
        """
            This method disconnects the client from a broker.
        """

        def on_disconnect(client, userdata, rc):
            """
            The Callback function.
            """
            print(rc)
            if rc != 0:
                print(f"Client {client_id} Unexpected disconnection.")
            else:
                print(f"Client {client_id} Disconnected!")

        mqtt_client.on_disconnect = on_disconnect
        client.disconnect()
        print(f"Client {client_id} Disconnected!")

    @abc.abstractmethod
    def run(self, client_id: int):
        """
        This method runs a client publisher or subscriber.
        :param client_id: int.
        :return:
        """

    def run_multiple(self, first_client_id=1):
        """
        This method runs self._nb_client client. For that, it uses multithreading. Each client, a thread.
        :param first_client_id: int.
        :return:
        """

        try:
            threads = list()
            for i in range(first_client_id, first_client_id + self._client_nb):
                x = threading.Thread(target=self.run, args=(i,))
                threads.append(x)
                x.start()

            for thread in threads:
                thread.join()

        except Exception as exception:
            print(exception)
