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
    

