# NETPIE API Documentation

Welcome to MicroPython NETPIE API Documentaion, This document will provide how to use each method inside the NETPIE Class.

## Import Class
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

### Example

```python
netpie_client = NETPIE()
netpie_client.set_profile("your_client_id", "your_token", "your_secret")

