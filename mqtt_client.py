import json
from umqtt.simple import MQTTClient
import config

class MQTTManager:
    """
    Manages MQTT connectivity, lifecycle states, and telemetry publishing.

    This class wraps the `umqtt.simple` client to provide simplified connection 
    handling, automatic 'Last Will and Testament' (LWT) management for 
    availability monitoring, and JSON-encoded state updates.

    Attributes:
        state_topic (bytes): Topic where telemetry/sensor data is published.
        avail_topic (bytes): Topic for LWT (online/offline status).
        connected (bool): Current connection status of the client.
    """

    def __init__(self, client_id, broker, port, state_topic, avail_topic, username=None, password=None):
        """
        Initialize the MQTT Manager with connection details and LWT.

        Args:
            client_id (str): Unique identifier for this MQTT client.
            broker (str): IP address or hostname of the MQTT broker.
            port (int): Port number (usually 1883 or 8883).
            state_topic (bytes): The MQTT topic for state updates.
            avail_topic (bytes): The MQTT topic for availability status.
            username (str, optional): Broker username. Defaults to None.
            password (str, optional): Broker password. Defaults to None.
        """
        self.state_topic = state_topic
        self.avail_topic = avail_topic
        self.connected = False

        self.client = MQTTClient(
            client_id=client_id,
            server=broker,
            port=port,
            user=username,
            password=password,
            keepalive=120
        )

        # Set Last Will: if the client drops unexpectedly, broker sends 'offline'
        self.client.set_last_will(self.avail_topic, b"offline", retain=True)

    def connect(self):
        """
        Establish connection to the broker and announce 'online' status.
        
        Raises:
            OSError: If the broker is unreachable or credentials are invalid.
        """
        self.client.connect()
        self.client.publish(self.avail_topic, b"online", retain=True)
        self.connected = True
        print("[MQTT] Connected")

    def publish_state(self, payload: dict):
        """
        Serialize a dictionary to JSON and publish it to the state topic.

        Args:
            payload (dict): The data structure to be sent to the broker.

        Raises:
            OSError: If called while the client is not connected.
        """
        if not self.connected:
            raise OSError("MQTT not connected")
        self.client.publish(self.state_topic, json.dumps(payload))

    def disconnect(self):
        """
        Gracefully shut down the connection.
        
        Publishes an 'offline' message to the availability topic before 
        closing the socket to ensure clean state transitions.
        """
        try:
            if self.connected:
                self.client.publish(self.avail_topic, b"offline", retain=True)
                self.client.disconnect()
        finally:
            self.connected = False