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

- `bool` : True if connected, False otherwise.

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

## `get_device_status(client_id=None, token=None)`

Get the specific device status using the NETPIE REST API.

## Parameters

- `client_id` (str, optional): The Client ID for authentication. Defaults to None.
- `token` (str, optional): The authentication token. Defaults to None.

If you already use `set_profile()`, then there is no need to pass `client_id` and `token` to this method.

But if you want to get the data of the different devices, then you need to specify the `client_id` and `token`.

### Returns

- `tuple`: A tuple containing the HTTP response code and device status data.

### Raises

- **NETPIEException:** If client_id or token is not a string or if there's an error with the API request.

### Example 1: without using set_profile()

```python

client_id = "your_client_id"
token = "your_token"

netpie_client = NETPIE()
response_code,data = netpie_client.get_device_status(client_id,token)
print("Response Code:",response_code)
print(data)

```

### Example 2: using set_profile()

```python

netpie_client = NETPIE()
netpie_client.set_profile("your_client_id","your_token")
response_code,data = netpie_client.get_device_status()
print("Response Code:",response_code)
print(data)

```

## `get_device_shadow(client_id=None, token=None)`

Get the Shadow data from a specific device using NETPIE's REST API.

## Parameters

- `client_id` (str, optional): The Client ID for authentication. Defaults to None.
- `token` (str, optional): The authentication token. Defaults to None.

If you already use `set_profile()`, then there is no need to pass `client_id` and `token` to this method.

But if you want to get the data of the different devices, then you need to specify the `client_id` and `token`.

### Returns

- `tuple`: A tuple containing the HTTP response code and Shadow data.

### Raises

- **NETPIEException:** If client_id or token is not a string or if there's an error with the API request.

### Example 1: without using set_profile()

```python

client_id = "your_client_id"
token = "your_token"

netpie_client = NETPIE()
response_code,data = netpie_client.get_device_shadow(client_id,token)
print("Response Code:",response_code)
print(data)

```

### Example 2: using set_profile()

```python

netpie_client = NETPIE()
netpie_client.set_profile("your_client_id","your_token")
response_code,data = netpie_client.get_device_shadow()
print("Response Code:",response_code)
print(data)

```

## `write_device_shadow(self, data, client_id=None, token=None)`

Write the provided data to the device Shadow using the NETPIE REST API.

## Parameters

- `data` (dict): The data to be written to the device shadow. Should be in the format:
                         {
                             "field name 1": value1,
                             "field name 2": value2,
                             ...,
                             "field name n": value n
                         }
- `client_id` (str, optional): The Client ID for authentication. Defaults to None.
- `token` (str, optional): The authentication token. Defaults to None.

If you already use `set_profile()`, then there is no need to pass `client_id` and `token` to this method.

But if you want to get the data of the different devices, then you need to specify the `client_id` and `token`.

### Returns
- `tuple`: A tuple containing the HTTP response text and response code.

### Raises
- **NETPIEException:** If data is not a dictionary, if client_id or token is not a string, or if there's an error with the API request.

### Example 1: without using set_profile()

```python

client_id = "your_client_id"
token = "your_token"
example_data = {"data1":123,"data2":"hello"}

netpie_client = NETPIE()
response_code,data = netpie_client.write_device_shadow(example_data,client_id,token)
print("Response Code:",response_code)
print(data)

```

### Example 2: using set_profile()

```python
example_data = {"data1":123,"data2":"hello"}

netpie_client = NETPIE()
netpie_client.set_profile("your_client_id","your_token")
response_code,data = netpie_client.write_device_shadow(example_data)
print("Response Code:",response_code)
print(data)

```

## `merge_device_shadow(self, data, client_id=None, token=None)`

Merge the provided data to the device Shadow using the NETPIE REST API.

## Parameters

- `data` (dict): The data to be written to the device shadow. Should be in the format:
                         {
                             "field name 1": value1,
                             "field name 2": value2,
                             ...,
                             "field name n": value n
                         }
- `client_id` (str, optional): The Client ID for authentication. Defaults to None.
- `token` (str, optional): The authentication token. Defaults to None.

If you already use `set_profile()`, then there is no need to pass `client_id` and `token` to this method.

But if you want to get the data of the different devices, then you need to specify the `client_id` and `token`.

### Returns

- `tuple`: A tuple containing the HTTP response text and response code.

### Raises

- **NETPIEException:** If data is not a dictionary, if client_id or token is not a string, or if there's an error with the API request.

### Example 1: without using set_profile()

```python

client_id = "your_client_id"
token = "your_token"
example_data = {"data1":123,"data2":"hello"}

netpie_client = NETPIE()
response_code,data = netpie_client.merge_device_shadow(example_data,client_id,token)
print("Response Code:",response_code)
print(data)

```

### Example 2: using set_profile()

```python
example_data = {"data1":123,"data2":"hello"}

netpie_client = NETPIE()
netpie_client.set_profile("your_client_id","your_token")
response_code,data = netpie_client.merge_device_shadow(example_data)
print("Response Code:",response_code)
print(data)

```

## `publish_private_message(topic,msg,client_id=None, token=None)`

Publishes a message to NETPIE's Private topic using the NETPIE REST API.

### Parameters

- `topic` (str): The topic to publish the message to.
- `msg` (str): The message to be published.
- `client_id` (str, optional): The Client ID for authentication. Defaults to None.
- `token` (str, optional): The authentication token. Defaults to None.

If you already use `set_profile()`, then there is no need to pass `client_id` and `token` to this method.

But if you want to get the data of the different devices, then you need to specify the `client_id` and `token`.

For the publisher, do not include the @private prefix in your topic; it will be filled in automatically.

For the subscriber,subscribe with @private/your_topic_name to receive the data.

### Returns

- `tuple`: A tuple containing the HTTP response text and response code.

### Raises

- **NETPIEException:** If topic, data, client_id, or token is not a string, or if there's an error with the API request.

### Example 1: without using set_profile()

```python

client_id = "your_client_id"
token = "your_token"
topic = "device1/data1"
message = "Hello"

netpie_client = NETPIE()
response_code,data = netpie_client.publish_private_message(topic,message,client_id,token)
print("Response Code:",response_code)
print(data)

```

### Example 2: using set_profile()

```python

topic = "device1/data1"
message = "Hello"

netpie_client = NETPIE()
netpie_client.set_profile("your_client_id","your_token")
response_code,data = netpie_client.publish_private_message(topic,message)
print("Response Code:",response_code)
print(data)

```

## `publish_device_message(topic,msg,client_id=None, token=None)`

Publishes data to NEPIE's Message topic using the NETPIE REST API.

### Parameters

- `topic` (str): The topic to publish the message to.
- `msg` (str): The message to be published.
- `client_id` (str, optional): The Client ID for authentication. Defaults to None.
- `token` (str, optional): The authentication token. Defaults to None.

If you already use `set_profile()`, then there is no need to pass `client_id` and `token` to this method.

But if you want to get the data of the different devices, then you need to specify the `client_id` and `token`.

For the publisher, do not include the @msg prefix in your topic; it will be filled in automatically.
 
For the subscriber,subscribe with @msg/your_topic_name to receive the data.

### Returns

- `tuple`: A tuple containing the HTTP response text and response code.

### Raises

- **NETPIEException:** If topic, data, client_id, or token is not a string, or if there's an error with the API request.

### Example 1: without using set_profile()

```python

client_id = "your_client_id"
token = "your_token"
topic = "device1/data1"
message = "Hello"

netpie_client = NETPIE()
response_code,data = netpie_client.publish_device_message(topic,message,client_id,token)
print("Response Code:",response_code)
print(data)

```

### Example 2: using set_profile()

```python

topic = "device1/data1"
message = "Hello"

netpie_client = NETPIE()
netpie_client.set_profile("your_client_id","your_token")
response_code,data = netpie_client.publish_device_message(topic,message)
print("Response Code:",response_code)
print(data)

```
