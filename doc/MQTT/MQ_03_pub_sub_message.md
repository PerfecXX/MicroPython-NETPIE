# Publishing data between the devices with Message Topic
This documentation will show you how to publish your message from one device to another with Message Topic using the MicroPython NETPIE library.

## Device Groupping
Make sure your devices are in the same group on the NETPIE platform.

![](https://github.com/PerfecXX/MicroPython-NETPIE/blob/main/doc/MQTT/doc_mqtt_03_device_groupping.jpg)

## Role Assignment 
The first device will publish the data to the second device by publishing the message to the same topic that the second device subscribes to.
If you want to add more devices, please make sure they are in the same group and subscribe to the same topic.

## NETPIE Message Topic
On the NETPIE platform, if you want to use the Message topic, any topic must be prefixed with @msg, but using this library, it will be automatically filled.
In this document, we will use **@msg/data** as the example message topic.


## The First Device Code (Publisher)

```python
# -----Import Library-----
from netpie import NETPIE
from network import WLAN,STA_IF
from time import sleep

# -----Network Credential-----
ssid="Your_WiFi_SSID"
password="Your_WiFi_Password"

# ----- Connect to WiFi Network-----
sta_if = WLAN(STA_IF)
sta_if.active(True)
if not sta_if.isconnected():
   print("Connecting to wifi: ", ssid)
   sta_if.connect(ssid, password)
   while not sta_if.isconnected():
       pass
print("Connection successful")

# -----Netpie Credentials-----
client_id = "Your_Client_ID"
token = "Your_Token"
secret = "Your_Secret"

# -----Begin Netpie Connection-----
netpie_client = NETPIE()
netpie_client.set_profile(client_id1,token1,secret1)
netpie_client.connect()
print("Netpie Connection Successful")

# -----Main Loop-----
while True:
    # ---Publish the data to NETPIE's Shadow-----
    netpie_client.publishMessage("@msg/data","Hello from device1")
    sleep(1)
    
```
In this code, the first device will publish the message "Hello from device 1" into the "@msg/data topic on the NETPIE.
If the second device subscribes to the same topic (**msg/data**), it will receive the message.

## The Second Device Code (Subscriber)

```python
# -----Import Library-----
from netpie import NETPIE
from network import WLAN,STA_IF
from time import sleep

# -----Network Credential-----
ssid="Your_WiFi_SSID"
password="Your_WiFi_Password"

# ----- Connect to WiFi Network-----
sta_if = WLAN(STA_IF)
sta_if.active(True)
if not sta_if.isconnected():
   print("Connecting to wifi: ", ssid)
   sta_if.connect(ssid, password)
   while not sta_if.isconnected():
       pass
print("Connection successful")

# ----- Callback Function-----
def on_message(topic,msg):
    topic,msg = topic.decode('utf8'),msg.decode('utf8')
    print('message from ',topic ,msg)

# -----Netpie Credentials-----
client_id = "Your_Client_ID"
token = "Your_Token"
secret = "Your_Secret"

# -----Begin Netpie Connection-----
netpie_client = NETPIE()
netpie_client.set_profile(client_id,token,secret)
netpie_client.set_callback(on_message)
netpie_client.connect()
print("Netpie Connection Successful")

# ----- Example Topic -----
topic1 = "@msg/data"
# ----- Subscribe Topic -----
netpie_client.subscribe(topic1)

# -----Main Loop-----
while True:
    # ----- Check out the message from the subscribed topic-----
    netpie_client.check_message()
    sleep(1)
```
Before the second device begins the connection with NETPIE, it will set the callback function named **on_message**.
This function will be called every time they receive a message from the subscribe topic.
When this function is called, it will show you the incoming topic and the message.

You need to set the callback function before starting the connection; otherwise,  it will not have any function to handle the incoming message.

After connecting with the NETPIE, you need to subscribe to the same topic as the first device (**@msg/data**).
In this library, you can subscribe to more than one topic at the same time.

Inside the loop, the second device must use **check_message()** to check the message in the NETPIE.
If there is a message in the subscribed topic, then the callback function will be called.
