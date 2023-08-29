# Import libraries
from simple import MQTTClient, MQTTException
from network import WLAN
import json
import urequests

__version__ = '1.0.0'
__author__ = 'Teeraphat Kullanankanjana'

# Class for NETPIE-related exceptions
class NETPIEException(Exception):
    pass

# Main class
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
        """
        Set the client profile with authentication details.

        Args:
            client_id (str): The Client ID for authentication.
            token (str, optional): The authentication token. Defaults to None.
            secret (str, optional): The authentication secret. Defaults to None.

        Raises:
            NETPIEException: If input types are invalid.
        """
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
    def connect(self, clean_session=True):
        """
        Connect to the NETPIE

        Args:
            clean_session (bool, optional): Whether to start with a clean session. Defaults to True.

        Raises:
            NETPIEException: If authentication details are missing or connection fails.
        """
        # Check for authentication details
        if self.client_id is None:
            raise NETPIEException("The Client ID must not be None before connecting.")
        
        if self.token is None:
            raise NETPIEException("The token must not be None before connecting.")
        
        if self.secret is None:
            raise NETPIEException("The secret must not be None before connecting.")
        
        try:
            # Attempt MQTT connection
            self.client.connect(clean_session=clean_session)
        except MQTTException as e:
            if e.errno == 5:
                raise NETPIEException("[MQTT Error 5] Not authorized.\nPlease check your Client ID, token, and secret.")
        except OSError as e:
            if e.errno == -202:
                if not WLAN().isconnected():
                    raise NETPIEException("[Error -202] Network Error.\nPlease check your internet or network connection.")
            
    def disconnect(self):
        """Disconnect from the NETPIE."""
        self.client.disconnect()
    
    def ping(self):
        """Ping the NETPIE."""
        self.client.ping()
    
    # Publish data to a specified topic
    def publish(self, topic, data):
        """
        Publish data to a specified topic.

        Args:
            topic (str): The topic to publish the data to.
            data: The data to be published.

        Raises:
            NETPIEException: If there's an error publishing the data.
        """
        try:
            # Publish data using the MQTT client
            self.client.publish(topic, data)
        except OSError as e:
            if e.errno == 104:
                raise NETPIEException("[Error 104] Connection reset.\nPlease ensure that your data publishing speed is not too fast.")

    # Publish shadow data
    def publishShadow(self, unformat_data):
        """
        Publish the data to Shadow Topic.

        Args:
            unformat_data (dict): The data to be published.

        Raises:
            NETPIEException: If the data format is invalid.
        """
        if not isinstance(unformat_data, dict):
            raise NETPIEException("The data must be a dictionary, but its type is {}".format(type(unformat_data)))
        # Wrap data in shadow format
        formatted_data = {"data": unformat_data}
        topic = self.shadow_topic + "data/update"
        # Publish formatted data
        self.publish(topic, json.dumps(formatted_data))

    # Publish a message to a specified topic
    def publishMessage(self, topic, unformat_message):
        """
        Publish a message to a specified topic.

        Args:
            topic (str): The topic to publish the message to.
            unformat_message (str): The message to be published.

        Raises:
            NETPIEException: If topic or message format is invalid.
        """
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
        """
        Set a callback function for incoming messages.

        Args:
            callback (function): The callback function to be set.

        Raises:
            NETPIEException: If the provided callback is not callable.
        """
        if callable(callback):
            self.client.set_callback(callback)
        else:
            raise NETPIEException("You must provide a valid callback function. Try removing () after the function name.")
    
    # Check for incoming messages
    def check_message(self):
        """Check for incoming messages."""
        self.client.check_msg()

    # Subscribe to a topic
    def subscribe(self, topic, qos=0):
        """
        Subscribe to a topic.

        Args:
            topic (str): The topic to subscribe to.
            qos (int, optional): Quality of Service level. Defaults to 0.

        Raises:
            NETPIEException: If the topic format is invalid.
        """
        if isinstance(topic, str):
            self.client.subscribe(topic, qos)
        else:
            raise NETPIEException("The topic must be a string.")
        
    def is_connected(self):
        """
        Check if the client is connected.

        Returns:
            bool: True if connected, False otherwise.
        """
        try:
            self.client.ping()
            return True
        except:
            return False
    
    def get_device_status(self, client_id=None, token=None):
        """
        Get the device status using the NETPIE REST API.

        Args:
            client_id (str, optional): The Client ID for authentication. Defaults to None.
            token (str, optional): The authentication token. Defaults to None.

        Returns:
            tuple: A tuple containing the HTTP response code and device status data.
        """
        if client_id is not None and not isinstance(client_id, str):
            raise NETPIEException("The client_id must be a string.")

        if token is not None and not isinstance(token, str):
            raise NETPIEException("The token must be a string.")
        
        if client_id is None:
            client_id = self.client_id
        
        if token is None:
            token = self.token
        
        endpoint = "https://api.netpie.io/v2/device/status"
        headers = {
            "Authorization": "Device {}:{}".format(client_id, token)}
        response = urequests.get(endpoint, headers=headers)
        response_text = response.text
        response_code = response.status_code
        response.close()

        if response_code == 200:
            try:
                status_data = json.loads(response_text)
                return response_code, status_data
            except json.JSONDecodeError as e:
                raise NETPIEException("Error decoding JSON response: {}".format(e))
        else:
            return response_code, response_text
    
    def get_device_shadow(self,client_id=None, token=None):
        """
        Get the device shadow data using the NETPIE REST API.

        Args:
            client_id (str, optional): The Client ID for authentication. Defaults to None.
            token (str, optional): The authentication token. Defaults to None.

        Returns:
            tuple: A tuple containing the HTTP response code and device shadow data.
        Raises:
            NETPIEException: If client_id or token is not a string or if there's an error with the API request.
        """
        if client_id is not None and not isinstance(client_id, str):
            raise NETPIEException("The client_id must be a string.")

        if token is not None and not isinstance(token, str):
            raise NETPIEException("The token must be a string.")
        
        if client_id is None:
            client_id = self.client_id
        
        if token is None:
            token = self.token
            
        endpoint = "https://api.netpie.io/v2/device/shadow/data"
        headers = {
            "Authorization": f"Device {client_id}:{token}"
            }
        response = urequests.get(endpoint, headers=headers)
        response_text = response.text
        response_code = response.status_code
        response.close()
        if response_code == 200:
            try:
                status_data = json.loads(response_text)
                return response_code, status_data
            except json.JSONDecodeError as e:
                raise NETPIEException("Error decoding JSON response: {}".format(e))
        else:
            return response_code, response_text
    
    def write_device_shadow(self, data, client_id=None, token=None):
        """
        Write the provided data to the device shadow using the NETPIE REST API.

        Args:
            data (dict): The data to be written to the device shadow. Should be in the format:
                         {
                             "field name 1": value1,
                             "field name 2": value2,
                             ...,
                             "field name n": value n
                         }
            client_id (str, optional): The Client ID for authentication. Defaults to None.
            token (str, optional): The authentication token. Defaults to None.

        Returns:
            tuple: A tuple containing the HTTP response text and response code.

        Raises:
            NETPIEException: If data is not a dictionary or if there's an error with the API request.
        """
        if not isinstance(data, dict):
            raise NETPIEException("The data must be a dictionary.")

        # Check if data is already formatted as expected
        if "data" not in data:
            formatted_data = {"data": data}
        else:
            formatted_data = data

        if client_id is None:
            client_id = self.client_id

        if token is None:
            token = self.token

        endpoint = "https://api.netpie.io/v2/device/shadow/data"
        headers = {
            "Authorization": f"Device {client_id}:{token}",
            "Content-Type": "application/json"}

        response = urequests.post(endpoint, headers=headers, json=formatted_data)
        response_text = response.text
        response_code = response.status_code
        response.close()

        if response_code == 200:
            try:
                status_data = json.loads(response_text)
                return response_code, status_data
            except json.JSONDecodeError as e:
                raise NETPIEException("Error decoding JSON response: {}".format(e))
        else:
            return response_code, response_text
    
    def merge_device_shadow(self, data, client_id=None, token=None):
        """
        Merge the provided data into the device shadow using the NETPIE REST API.

        Args:
            data (dict): The data to be merged into the device shadow. Should be in the format:
                         {
                             "field name 1": value1,
                             "field name 2": value2,
                             ...,
                             "field name n": value n
                         }
            client_id (str, optional): The Client ID for authentication. Defaults to None.
            token (str, optional): The authentication token. Defaults to None.

        Returns:
            tuple: A tuple containing the HTTP response text and response code.

        Raises:
            NETPIEException: If data is not a dictionary or if there's an error with the API request.
        """
        if not isinstance(data, dict):
            raise NETPIEException("The data must be a dictionary.")

        # Check if data is already formatted as expected
        if "data" not in data:
            formatted_data = {"data": data}
        else:
            formatted_data = data

        if client_id is None:
            client_id = self.client_id

        if token is None:
            token = self.token

        endpoint = "https://api.netpie.io/v2/device/shadow/data"
        headers = {
            "Authorization": f"Device {client_id}:{token}",
            "Content-Type": "application/json"}

        response = urequests.put(endpoint, headers=headers, json=formatted_data)
        response_text = response.text
        response_code = response.status_code
        response.close()

        if response_code == 200:
            try:
                status_data = json.loads(response_text)
                return response_code, status_data
            except json.JSONDecodeError as e:
                raise NETPIEException("Error decoding JSON response: {}".format(e))
        else:
            return response_code, response_text
    
    def publish_private_message(self,topic,msg,client_id=None, token=None):
        """
        Publishes a message to NETPIE's Private topic using the NETPIE REST API.
        For the publisher, do not include the @private prefix in your topic; it will be filled in automatically.
        For the subscriber,subscribe with @private/your_topic_name to receive the data.
        
        Args:
            topic (str): The topic to publish the message to.
            msg (str): The message to be published.
            client_id (str, optional): The Client ID for authentication. Defaults to None.
            token (str, optional): The authentication token. Defaults to None.

        Returns:
            tuple: A tuple containing the HTTP response text and response code.
        Raises:
            NETPIEException: If topic or message format is invalid.
        """
        if not isinstance(topic, str):
            raise NETPIEException("The topic must be a string.")
        
        if not isinstance(msg, str):
            raise NETPIEException("The message must be a string.")
        
        if topic.startswith("@private/"):
            raise NETPIEException("Do not include the '@private/' prefix in the topic.")
        
        if client_id is None:
            client_id = self.client_id
        
        if token is None:
            token = self.token
        endpoint = "https://api.netpie.io/v2/device/private/{}".format(topic)
        headers = {
            "Authorization": f"Device {client_id}:{token}",
            "Content-Type": "text/plain"}
        response = urequests.put(endpoint, headers=headers, data=msg)
        response_text = response.text
        response_code = response.status_code
        response.close()
        return response_text,response_code
        
    
    def publish_device_message(self,topic,msg,client_id=None,token=None):
        """
        Publishes data to NEPIE's Message topic using the NETPIE REST API.
        For the publisher, do not include the @msg prefix in your topic; it will be filled in automatically.
        For the subscriber,subscribe with @msg/your_topic_name to receive the data.

        Args:
            topic (str): The topic to publish the message to.
            msg (str): The message to be published.
            client_id (str, optional): The Client ID for authentication. Defaults to None.
            token (str, optional): The authentication token. Defaults to None.

        Returns:
            tuple: A tuple containing the HTTP response text and response code.
        Raises:
            NETPIEException: If topic or message format is invalid.
        """
        
        if not isinstance(topic, str):
            raise NETPIEException("The topic must be a string.")
        
        if not isinstance(msg, str):
            raise NETPIEException("The message must be a string.")
        if topic.startswith("@msg/"):
            raise NETPIEException("Do not include the '@msg/' prefix in the topic.")
        
        if client_id is None:
            client_id = self.client_id
        
        if token is None:
            token = self.token
            
        endpoint = "https://api.netpie.io/v2/device/message/{}".format(topic)
        headers = {
            "Authorization": f"Device {client_id}:{token}",
            "Content-Type": "text/plain"}
        response = urequests.put(endpoint, headers=headers, data=msg)
        response_text = response.text
        response_code = response.status_code
        response.close()
        return response_text,response_code

