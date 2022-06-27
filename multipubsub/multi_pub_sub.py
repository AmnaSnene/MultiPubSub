import abc
import random
import threading
import multipubsub.tools as tools
from datetime import datetime
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
    topics_nb is the number of topic to publish on or to subscribe to. Defaults to 1.
    new_topics is boolean value. If new_topics is true, the program creates new topics else it uses topics_file.
    """

    def __init__(self, host="localhost", port=1883, client_nb=1, topics_nb=1, new_topics=False):
        self._host = host
        self._port = port
        self._client_nb = client_nb
        self._topics = None
        self._qos = 0
        self._duration_to_disconnect = 0
        self._topics_nb = topics_nb
        self._new_topics = new_topics

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

    def set_topic(self):
        """
        If self.topics is None, the program chooses randomly topics from topics_file or creates new topics.
        If the number of topics > the number of the topics in the topics_file, the program takes all the topics in the
        topics_file and generates the rest.
        :return:
        """
        if self.topics is None and not self._new_topics:

            f = open("topics_file")
            list_topic = f.readlines()
            f.close()
            diff = self._topics_nb - len(list_topic)
            if diff > 0:
                self.topics = list_topic + tools.get_new_topic(diff)
            else:
                # random index list in the range of 0, len(list_topic)
                random_index = random.sample(range(len(list_topic)), self._topics_nb)
                self.topics = [list_topic[i] for i in random_index]
        elif self.topics is None and self._new_topics:
            self.topics = tools.get_new_topic(self._topics_nb)

    def connect_mqtt(self, client_id: str) -> mqtt_client:
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
                print(f"{client_id} Connected to MQTT Broker!")
            else:
                print(f"{client_id} Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client('{}'.format(client_id))
        client.on_connect = on_connect
        client.connect(self._host, self._port)
        return client

    def disconnect_mqtt(self, client: mqtt_client, client_id: str):
        """
            This method disconnects the client from a broker.
        """

        def on_disconnect(client, userdata, rc):
            """
            The Callback function.
            """
            print(rc)
            if rc != 0:
                print(f"{client_id} Unexpected disconnection.")
            else:
                print(f"{client_id} Disconnected!")

        mqtt_client.on_disconnect = on_disconnect
        client.disconnect()
        print(f"{client_id} Disconnected!")

    @abc.abstractmethod
    def run(self, client_id: str):
        """
        This method runs a client publisher or subscriber.
        :param client_id: str.
        :return:
        """

    def run_multiple(self):
        """
        This method runs self._nb_client client. For that, it uses multithreading. Each client, a thread.
        :return:
        """
        self.set_topic()
        try:
            threads = list()
            for i in range(self._client_nb):
                client_id = tools.get_client_id()
                x = threading.Thread(target=self.run, args=(client_id,))
                threads.append(x)
                x.start()

            for thread in threads:
                thread.join()

        except Exception as exception:
            print(exception)
