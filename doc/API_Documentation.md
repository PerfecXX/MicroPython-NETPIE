# NETPIE API Documentation

Welcome to MicroPython NETPIE API Documentaion, This document will provide how to use each method inside the NETPIE Class.

## `Import Class`
Before using NETPIE Class, you need to import the library first.

```python
# Import Library
from netpie import NETPIE
```

## `NETPIE()`

To interact with the NETPIE IoT platform, you need to create an instance of the `NETPIE` class.

### Example

```python
from netpie import NETPIE

# Create an instance of the NETPIE class
netpie_client = NETPIE()
```

## `set_profile(client_id, token=None, secret=None)`

Set the client profile with authentication details.

You can get your client_id, token, and secret from a device on the NETPIE platform.

### Parameters

- `client_id` (str): The Client ID for authentication.
- `token` (str, optional): The authentication token. Defaults to None.
- `secret` (str, optional): The authentication secret. Defaults to None.

If you are using MQTT, all of them will be required.

If you are using the REST API, both the client_id and token will be required.

### Raises
- **NETPIEException**: If credential types are invalid.

### Example

```python
netpie_client = NETPIE()
netpie_client.set_profile("your_client_id", "your_token", "your_secret")
```

## `Connect(clean_session=True)`

Connect to the NETPIE by using the setting credential.

Use this method only when connecting a device to NETPIE with MQTT.

- You need to use `set_profile()` before connecting to NETPIE.
- You device need to access the internet before connecting to NETPIE

### Parameters
- `clean_session` (bool, optional): Whether to start with a clean session. Defaults to True.

### Raises
- **NETPIEException**: If authentication details are missing or the connection fails.
- **NETPIEException([MQTT Error 5])**: If MQTT authentication fails, it might be because of a missing or invalid credential.
- **NETPIEException([Error -202])**: If there's a network error or no access to the internet.

### Example
```python
netpie_client = NETPIE()
netpie_client.set_profile("your_client_id", "your_token", "your_secret")
netpie_client.connect()
```

## `publishShadow(unformat_data)`

Publish the data to NETPIE's Shadow Topic.

The published data will be stored in NETPIE's Shadow.

Use this method only when connecting a device to NETPIE with MQTT and only after successful connection.

### Parameters
- `unformat_data` (dict): The data to be published.

### Raises
- **NETPIEException:** If the data is not dict or JSON.

### Example
```python
example_data = {"data1":"test","data2":1723}

netpie_client = NETPIE()
netpie_client.set_profile("your_client_id", "your_token", "your_secret")
netpie_client.connect()
netpie_client.publishShadow(example_data)
```

## `publishMessage(topic, unformat_message)`

Publish a single string message to a specific NETPIE message topic.

Use this method only when connecting a device to NETPIE with MQTT and only after successful connection.

### Parameters
- `topic` (str): The topic to publish the message to. The topic will be prefixed with @msg/.
- `unformat_message` (str): The message to be published.

### Raises
- **NETPIEException:** If topic or message format is invalid.

### Example
```python
example_msg = "Hello"

netpie_client = NETPIE()
netpie_client.set_profile("your_client_id", "your_token", "your_secret")
netpie_client.connect()
netpie_client.publishMessage(example_msg)
```

## `set_callback(callback)`

Set a callback function for incoming messages.

Use this method only when connecting a device to NETPIE with MQTT and only before using `connect()`.

### Parameters
- `callback` (function): Set a callback function for incoming messages.

### Raises
- **NETPIEException:** If the provided callback is not callable.

### Example
```python
def on_message(topic,msg):
    topic,msg = topic.decode('utf8'),msg.decode('utf8')
    print('message from ',topic ,msg)

netpie_client = NETPIE()
netpie_client.set_profile("your_client_id", "your_token", "your_secret")
netpie_client.set_callback(on_message)
netpie_client.connect()
```

## `subscribe(topic, qos=0)`

Subscribe to a topic.

You can subscribe to more than one topic at the same time.

The topic must be prefixed with the following to get the data in the NETPIE topic:
- @msg/your_topic_name: for a message from NETPIE
- @private/# : for receive all information on the topic beginning with @private/.
- @private/shadow/data/get/response : for receive device shadow information, when it is requested.

Use this method only when connecting a device to NETPIE with MQTT and only before using `connect()`.

### Parameters
-  `topic` (str): The topic to subscribe to.
-  `qos` (int, optional): Quality of Service level. Defaults to 0.

### Raises
- `NETPIEException:` If the topic format is invalid.

### Example
```python
def on_message(topic,msg):
    topic,msg = topic.decode('utf8'),msg.decode('utf8')
    print('message from ',topic ,msg)

topic1 = "@msg/device1/data1"
topic2 = "@msg/device1/data2"
topic3 = "@private/#"

netpie_client = NETPIE()
netpie_client.set_profile("your_client_id", "your_token", "your_secret")
netpie_client.set_callback(on_message)
netpie_client.subscribe(topic1)
netpie_client.subscribe(topic2)
netpie_client.subscribe(topic3)
netpie_client.connect()
```

## `check_message()`

Check for incoming messages.

Use this method only when connecting a device to NETPIE with MQTT and only after setting the callback function, subscribing to Topic, and making a successful connection.

Use this method inside your main loop to continue checking the message.

If you don't call this method, the device will not receive any messages from NETPIE.

### Example
```python
def on_message(topic,msg):
    topic,msg = topic.decode('utf8'),msg.decode('utf8')
    print('message from ',topic ,msg)

topic1 = "@msg/device1/data1"

netpie_client = NETPIE()
netpie_client.set_profile("your_client_id", "your_token", "your_secret")
netpie_client.set_callback(on_message)
netpie_client.subscribe(topic1)

while True:
    netpie_client.check_message()
```

## `is_connected()`

Check if the device client is connected to NETPIE.

Use this method only when connecting a device to NETPIE with MQTT.

### Returns
- `True` : if connected
- `False` : if not connected

### Example
```python
netpie_client = NETPIE()
status = netpie_client.is_connected()
print("Netpie Status: ",status)
```


## `disconnect()`

Disconnect from the NETPIE.

Use this method when connecting NETPIE with MQTT.

### Example
```python
netpie_client = NETPIE()
netpie_client.set_profile("your_client_id", "your_token", "your_secret")
netpie_client.connect()
netpie_client.disconnect()
```


