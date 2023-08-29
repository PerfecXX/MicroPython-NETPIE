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
    # Check the messages sent from NETPIE.
    netpie_client.check_message()
    # ----- Example Data-----
    message = "Your number is {}".format(randint(0,100))
    
    # ---Publish the data to your topic-----
    netpie_client.publishMessage(topic1,message)

    sleep(1)
    

