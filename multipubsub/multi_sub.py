from time import sleep
import multipubsub.tools as tools
from multipubsub.multi_pub_sub import PubSub
from paho.mqtt import client as mqtt_client


class Sub(PubSub):

    def __init__(self, host="localhost", port=1883, client_nb=1, topics_nb=1):
        self._duration_to_unsubscribe = 0
        PubSub.__init__(self, host=host, port=port, client_nb=client_nb, topics_nb=topics_nb)

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

    def subscribe(self, client: mqtt_client, client_id: str):
        """
        This method subscribes the client to one or multiple topics.
        """

        def on_message(client, userdata, msg):
            """
            The callback function.
            """

            tools.calculate_latency(tools.unpack_msg(msg.payload), client)
            #print(f"{client_id} Received from `{msg.topic}` topic")
            # print("recieved")

        def on_subscribe(client, userdata, mid, granted_qos):
            print(f"Subscribed{client_id}")

        client.on_subscribe = on_subscribe
        subscription_list = [(topic, self.qos) for topic in self.topics]
        client.subscribe(subscription_list)
        client.on_message = on_message

    def unsubscribe(self, client: mqtt_client, client_id: str):
        """
         This method unsubscribes the client from self.topics.
        """

        def on_unsubscribe(client, userdata, mid):
            """
            The callback function.
            """
            print(f"{client_id}unsubscribed from {self.topics}")

        client.on_unsubscribe = on_unsubscribe
        client.unsubscribe(self.topics)

    def run_client(self, client_id: str):
        """
        This method runs a client publisher or subscriber.
        :param client_id: str.
        :return:
        """
        client = self.connect_mqtt(client_id)
        self.subscribe(client, client_id)

        client.loop_start()
        while 1:
            if self.duration_to_unsubscribe:
                sleep(self.duration_to_unsubscribe)
                self.unsubscribe(client, client_id)
            if self.duration_to_disconnect:
                sleep(self.duration_to_disconnect)
                self.disconnect_mqtt(client, client_id)
                client.loop_stop()
                break
            sleep(1)
