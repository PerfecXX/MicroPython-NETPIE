# Connection to Netpie with MQTT 
This documentation will show you how to connect your device to NETPIE via MQTT using the MicroPython NETPIE library.

## Import the Library

```python
from netpie import NETPIE
from network import WLAN,STA_IF
from time import sleep
```
In this section, the necessary libraries are being imported. 
1. netpie library is used to connect to the NETPIE platform.
2. network library is used for wifi connection. 
3. time library provides functions for delay.

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

## Main Loop

```python
while True:
    # add_your_code_here
    sleep(1)
```
Finally, this is the main loop of your program. It runs indefinitely (while True:), 
and you can add your own code within this loop. The sleep(1) function call causes the program to pause for 1 second in each iteration of the loop. 
This can be helpful to avoid excessive use of resources and to introduce a delay between iterations.

## Back to NETPIE 
Go back to your device on the NETPIE, and the device's status should become online.

## Full code
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
netpie_client.set_profile(client_id,token,secret)
netpie_client.connect()
print("Netpie Connection Successful")

# -----Main Loop-----
while True:
    # add_your_code_here
    sleep(1)
```
