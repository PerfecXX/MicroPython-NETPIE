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
    

