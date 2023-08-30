# Control your device with NETPIE's Dashboard.
This documentation will show you how to control your device with a NETPIE widget using the MicroPython NETPIE library.
The device will publish the example data to NETPIE, and NETPIE can send the message command back to the device.

## Dashboard Setting 
Create your NETPIE dashboard, then go to Settings and add the device.
Make sure your device privileges are **Subscribe Message** and **Publish Message**.

![](https://github.com/PerfecXX/MicroPython-NETPIE/blob/main/doc/MQTT/doc_mqtt_04_device_privileges.jpg)

## The code 
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
    # ----- Example Data -----
    payload = {"temperature":randint(0,100),
           "humidity":randint(0,100),
           "movement":{
               "X":randint(0,360),
               "Y":randint(0,360),
               "Z":randint(0,360)
               }}
    # ---Publish the data to NETPIE's Shadow-----
    netpie_client.publishShadow(payload)
    sleep(1)
    
```

In this code, the device will publish the example data to NETPIE's Shadow, and it will also subscribe to the topic **@msg/data**.This topic is an example of how to communicate between NETPIE and the device.

## Show the Shadow data in the NETPIE dashboard.

Add the **Text** widget and set the value to the device that you want to show by clicking **device** > **Shadow** > **Your data**

In this example, we will set the temperature and humidity.

![](https://github.com/PerfecXX/MicroPython-NETPIE/blob/main/doc/MQTT/doc_mqtt_05_widget_setting1.jpg)
![](https://github.com/PerfecXX/MicroPython-NETPIE/blob/main/doc/MQTT/doc_mqtt_05_widget_setting2.jpg)
![](https://github.com/PerfecXX/MicroPython-NETPIE/blob/main/doc/MQTT/doc_mqtt_05_widget_shaodw.jpg)

## Send the message from NETPEI Widget
Add the **Button** widget, then set **ON CLICK ACTION** by clicking **Device** and selecting **.publishMsg().**
In.publishMsg(), the first parameter is the **topic** that you want to send, and the second parameter is the **message** you want to send.
In the widget setting, the topic needs to **remove the @msg prefix.**
In this example, your device is subscribed to @msg/data, so in the button widget, the topic is changed to **"data".**

![](https://github.com/PerfecXX/MicroPython-NETPIE/blob/main/doc/MQTT/doc_mqtt_05_widget_button_setting.jpg)

When you click the button, NETPIE will publish the message to the topic (in this example, "data" after removing the @msg prefix).
If your device subscribes to the same topic (@msg/data), then it will receive the message data.

![](https://github.com/PerfecXX/MicroPython-NETPIE/blob/main/doc/MQTT/doc_mqtt_05_receive_data.jpg)

