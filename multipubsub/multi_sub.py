from time import sleep

from multipubsub.multi_pub_sub import PubSub

from paho.mqtt import client as mqtt_client


class Sub(PubSub):

    def __init__(self, host="localhost", port=1883, client_nb=1):
        self._duration_to_unsubscribe = 0
        super(Sub, self).__init__()

    """
       If you want to unsubscribe from all the topics after n seconds, you should change the default value of the attribute
       duration_to_unsubscribe. Defaults to 0.
       """

    @property
    def duration_to_unsubscribe(self):
        return self._duration_to_unsubscribe

    @duration_to_unsubscribe.setter
    def duration_to_unsubscribe(self, duration_to_unsubscribe: int) -> None:
        self._duration_to_unsubscribe = duration_to_unsubscribe

    def subscribe(self, client: mqtt_client, client_id: int):
        """
        This method subscribes the client to one or multiple topics.
        """

        def on_message(client, userdata, msg):
            """
            The callback function.
            """
            print(f"Client{client_id} Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        subscription_list = [(topic, self.qos) for topic in self.topics]
        client.subscribe(subscription_list)
        client.on_message = on_message

    def unsubscribe(self, client: mqtt_client, client_id):
        """
         This method unsubscribes the client from self.topics.
        """

        def on_unsubscribe(client, userdata, mid):
            """
            The callback function.
            """
            print("unsubscribed from {}".format(self.topics))

        client.on_unsubscribe = on_unsubscribe
        client.unsubscribe(self.topics)

    def run(self, client_id: int):
        """
        This method runs a client publisher or subscriber.
        :param client_id: int.
        :return:
        """
        client = self.connect_mqtt(client_id)
        self.subscribe(client, client_id)
        client.loop_start()
        if self.duration_to_unsubscribe:
            sleep(self.duration_to_unsubscribe)
            self.unsubscribe(client, client_id)
        if self.duration_to_disconnect:
            sleep(self.duration_to_disconnect)
            self.disconnect_mqtt(client, client_id)
            client.loop_stop()
