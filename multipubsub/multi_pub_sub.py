import abc
import threading
import multipubsub.tools as tools
from abc import ABC
from paho.mqtt import client as mqtt_client


class PubSub(ABC):
    """
    This class allows to create multiple MQTT publishers or subscribers with the same behavior.
    This can be useful for benchmarking MQTT Broker performances.

    host is the hostname or IP address of the remote broker. Defaults to localhost.
    port is the network port of the server host to connect to. Defaults to 1883.

    client_nb is the number of clients (publishers or subscribers). Defaults to 1.
    topics_nb is the number of topic to publish on or to subscribe to. Defaults to 1.
    """

    def __init__(self, host="localhost", port=1883, client_nb=1, topics_nb=1, ):
        self._host = host
        self._port = port
        self._client_nb = client_nb
        self._topics = None
        self._qos = 0
        self._duration_to_disconnect = None
        self._topics_nb = topics_nb
        self._current_client = []

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

    @property
    def client_nb(self):
        return self._client_nb

    @client_nb.setter
    def client_nb(self, client_nb: int):
        self._client_nb = client_nb

    @property
    def topics_nb(self):
        return self._topics_nb

    @topics_nb.setter
    def topics_nb(self, topics_nb: int):
        self._topics_nb = topics_nb

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

    def _set_topics(self):
        """
        :return:
        """
        if self.topics is None:
            self.topics = [f"topic{i}" for i in range(self._topics_nb)]

    def connect_mqtt(self, client_id: str) -> mqtt_client:
        """
        This method connects the client to a broker.
        param client_id:
        :return:
        """
        client = mqtt_client.Client(client_id)
        print('client')
        # client.on_connect = on_connect
        client.connect(self._host, self._port)
        print('connected')
        return client

    @staticmethod
    def disconnect_mqtt(client: mqtt_client):
        """
            This method disconnects the client from a broker.
        """
        # mqtt_client.on_disconnect = on_disconnect
        client.disconnect()

    @abc.abstractmethod
    def run_client(self, client: mqtt_client):
        """
        This method runs a client publisher or subscriber.
        param client_id: str.
        :return:
        """

    def update_client_list(self):
        difference_client = len(self._current_client) - self._client_nb
        print(abs(difference_client))
        if difference_client < 0:
            for i in range(abs(difference_client)):
                print("append")
                id = tools.get_client_id()
                print(id)
                client = self.connect_mqtt(id)
                print('connect')
                self._current_client.append(client)
        else:
            for i in range(difference_client):
                client = self._current_client.pop()
                self.disconnect_mqtt(client)

    def run_multiple(self):
        """
        This method runs self._nb_client client. For that, it uses multithreading. Each client, a thread.
        :return:
        """
        self._set_topics()
        print(self._topics)
        try:
            threads = list()
            self.update_client_list()
            print(self._current_client)
            for i in self._current_client:
                x = threading.Thread(target=self.run_client, args=(i,))
                threads.append(x)
                x.start()

            for thread in threads:
                thread.join()

        except Exception as exception:
            print(exception)
