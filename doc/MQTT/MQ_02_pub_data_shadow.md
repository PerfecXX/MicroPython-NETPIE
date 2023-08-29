# Publish the data to NETPIE with a shadow topic.
This documentation will show you how to publish your data to NEPIE with a Shadow Topic via MQTT using the MicroPython NETPIE library.

## Import the Library

```python
from netpie import NETPIE
from network import WLAN,STA_IF
from time import sleep
from random import randint
```
In this section, the necessary libraries are being imported. 
1. netpie library is used to connect to the NETPIE platform.
2. network library is used for wifi connection.
3. time library provides functions for delay.
4. random library is used for generate random numbers.

## Connect your device to your WiFi
Before you connect to NETPIE Make sure your device is already connected to the internet.

```python
ssid="replace_with_your_wifi_ssid"
password="replace_with_your_wifi_password"

sta_if = WLAN(STA_IF)
sta_if.active(True)
if not sta_if.isconnected():
   print("Connecting to wifi: ", ssid)
   sta_if.connect(ssid, password)
   while not sta_if.isconnected():
       pass
print("Connection successful")
```
## NETPIE Device Credential 
A unique key is required to connect a device to the platform. 
The key associated with the device can be viewed on the platform portal.

```python
client_id = "Your_Client_ID"
token = "Your_Token"
secret = "Your_Secret"
```
## Declare Netpie Instance

```python
netpie_client = NETPIE()
netpie_client.set_profile(client_id,token,secret)
netpie_client.connect()
print("Netpie Connection Successful")
```

This section establishes a connection to the NETPIE platform using the credentials you provided earlier. 
It creates a NETPIE client object, sets the profile using the client ID, token, and secret, and then establishes the connection to the NETPIE platform.

## Example Data

```python
payload = {"temperature":randint(0,100),
           "humidity":randint(0,100),
           "movement":{
               "X":randint(0,360),
               "Y":randint(0,360),
               "Z":randint(0,360)
               }}
```
**The data needs to be in JSON or dict format.**

## Publish the data

```python
while True:
    netpie_client.publishShadow(payload)
    sleep(1)
```
Inside the loop, it sends the example data to the NETPIE platform using the publishShadow() method. 
After sending the data, it waits for 1 second before sending the next set of data. 
This loop continues indefinitely, simulating a device continuously sending sensor data to NETPIE.

## Back to NETPIE
Go back to your device on the NETPIE, and the device's status should become online.
You can see the example data in the Shadow tab.

![](https://github.com/PerfecXX/MicroPython-NETPIE/blob/main/doc/MQTT/doc_mqtt_02_example_data_in_shadow.jpg)

## Full Code
```python
# -----Import Library-----
from netpie import NETPIE
from network import WLAN,STA_IF
from time import sleep
from random import randint

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
netpie_client.set_profile(client_id,token,secret)
netpie_client.connect()
print("Netpie Connection Successful")

# ----- Example Data -----
payload = {"temperature":randint(0,100),
           "humidity":randint(0,100),
           "movement":{
               "X":randint(0,360),
               "Y":randint(0,360),
               "Z":randint(0,360)
               }}

# -----Main Loop-----
while True:
    # ---Publish the data to NETPIE's Shadow-----
    netpie_client.publishShadow(payload)
    sleep(1)
    
```
