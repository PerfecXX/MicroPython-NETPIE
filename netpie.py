# Import Library
from simple import MQTTClient, MQTTException
import json

__version__ = '0.0.1'
__author__ = 'Teeraphat Kullanankanjana'

# NETPIE Exception Class
class NETPIEException(Exception):
    pass

# Main class for interacting with the NETPIE platform
class NETPIE:
    def __init__(self):
        # Default MQTT broker information
        self.hostname = "mqtt.netpie.io"
        self.port = 1883
        # Topic formats for messages and shadows
        self.msg_topic = "@msg/"
        self.shadow_topic = "@shadow/"
        # Initialize client attributes
        self.client = None
        self.client_id = None
        self.token = None
        self.secret = None
    
    # Set the client profile with authentication details
    def set_profile(self, client_id, token=None, secret=None):
        # Validate input types
        if not isinstance(client_id, str):
            raise NETPIEException("The Client ID must be a string.")

        if token is not None and not isinstance(token, str):
            raise NETPIEException("The token must be a string.")

        if secret is not None and not isinstance(secret, str):
            raise NETPIEException("The secret must be a string.")

        # Set client attributes
        self.client_id = client_id
        self.token = token
        self.secret = secret
        self.client = MQTTClient(self.client_id, self.hostname, user=self.token, password=self.secret)

    # Connect to the MQTT broker
    def connect(self):
        # Check for authentication details
        if self.client_id is None:
            raise NETPIEException("The Client ID must not be None before connecting.")
        
        if self.token is None:
            raise NETPIEException("The token must not be None before connecting.")
        
        if self.secret is None:
            raise NETPIEException("The secret must not be None before connecting.")
        
        try:
            # Attempt MQTT connection
            self.client.connect()
        except MQTTException as e:
            if e.errno == 5:
                raise NETPIEException("[MQTT Error 5] Not authorized.\nPlease check your Client ID, token, and secret.".format(e.errno))
            
    # Publish data to a specified topic
    def publish(self, topic, data):
        try:
            # Publish data using the MQTT client
            self.client.publish(topic, data)
        except OSError as e:
            if e.errno == 104:
                raise NETPIEException("[Error 104] Connection reset.\nPlease ensure that your data publishing speed is not too fast.")

    # Publish shadow data
    def publishShadow(self, unformat_data):
        if not isinstance(unformat_data, dict):
            raise NETPIEException("The data must be a dictionary, but its type is {}".format(type(unformat_data)))
        # Wrap data in shadow format
        formatted_data = {"data": unformat_data}
        topic = self.shadow_topic + "data/update"
        # Publish formatted data
        self.publish(topic, json.dumps(formatted_data))

    # Publish a message to a specified topic
    def publishMessage(self, topic, unformat_message):
        if not isinstance(topic, str):
            raise NETPIEException("The topic must be a string.")

        if not topic.startswith("@msg/"):
            topic = "@msg/" + topic

        if isinstance(unformat_message, str):
            # Publish the message
            self.publish(topic, unformat_message)
        else:
            raise NETPIEException("The data must be a string.")

    # Set a callback function for incoming messages
    def set_callback(self, callback):
        if callable(callback):
            self.client.set_callback(callback)
        else:
            raise NETPIEException("You must provide a valid callback function. Try removing () after the function name.")
    
    # Check for incoming messages
    def check_message(self):
        self.client.check_msg()

    # Subscribe to a topic
    def subscribe(self, topic):
        if isinstance(topic, str):
            self.client.subscribe(topic)
        else:
            raise NETPIEException("The topic must be a string.")

