import threading
import schedule
import time
import multipubsub.tools as tools

from multipubsub.multi_pub_sub import PubSub

from paho.mqtt import client as mqtt_client


class Pub(PubSub):

    def __init__(self, host="localhost", port=1883, client_nb=1, topics_nb=1):
        self._msg_per_second = 1
        self._publishing_duration = None
        self._msg_size = 1
        PubSub.__init__(self, host=host, port=port, client_nb=client_nb, topics_nb=topics_nb)

    @property
    def msg_per_second(self):
        return self._msg_per_second

    @msg_per_second.setter
    def msg_per_second(self, msg_per_second: int) -> None:
        self._msg_per_second = msg_per_second

    @property
    def publishing_duration(self):
        return self._publishing_duration

    @publishing_duration.setter
    def publishing_duration(self, publishing_duration: int) -> None:
        self._publishing_duration = publishing_duration

    @property
    def msg_size(self):
        return self._msg_size

    @msg_size.setter
    def msg_size(self, msg_size: int) -> None:
        self._msg_size = msg_size

    def publish_per_second(self, client: mqtt_client, topic: str):
        for i in range(self.msg_per_second * 2):
            msg = tools.create_msg(self.msg_size)
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]

            if status == 0:
                # pass
                print(f"{client._client_id.decode()} Send to topic `{topic}`")
            else:
                print(f"{client._client_id.decode()} Failed to send message to topic {topic}")

    def publish(self, client: mqtt_client,  topic: str) -> None:
        """
        """
        schedule.every(2).second.do(self.publish_per_second, client=client, topic=topic)
        t_end = tools.get_t_end_publishing(self.duration_to_disconnect, self.publishing_duration) + time.time()
        while time.time() <= t_end:
            schedule.run_pending()
            time.sleep(1)
        try:
            if t_end == self.duration_to_disconnect + 1:
                self.disconnect_mqtt(client)
        except:
            pass

    def run_client(self, client_mqtt: mqtt_client):
        try:
            threads = list()
            for topic in self.topics:
                x = threading.Thread(target=self.publish, args=(client_mqtt, topic))
                threads.append(x)
                x.start()

            for thread in threads:
                thread.join()

        except Exception as exception:
            print(exception)
