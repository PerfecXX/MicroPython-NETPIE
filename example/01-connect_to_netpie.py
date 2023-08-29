# -----Import Library-----
from netpie import NETPIE
from network import WLAN,STA_IF

# -----Network Credential-----
ssid="iMakeEDU"
password="imake1234"

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
client_id = "b36d57dd-7a74-44a0-be2e-88a643b41b60"
token = "LFMmCBeNuK5wrC1sj2qt5gfNKAf5s6Yb"
secret = "5ikhwLpwNg8KkYWEPf9tvrGTuHhwRgVX"

# -----Begin Netpie Connection-----
netpie_client = NETPIE()
netpie_client.set_profile(client_id,token,secret)
netpie_client.connect()

# -----Main Loop-----
while True:
    # your_code_here
    pass
