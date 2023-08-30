# NETPIE API Documentation

Welcome to MicroPython NETPIE API Documentaion, This document will provide how to use each method inside the NETPIE Class.

## Import Class
Before using NETPIE Class, you need to import the library first.

```python
# Import Library
from netpie import NETPIE
```

## Class Instance

To interact with the NETPIE IoT platform, you need to create an instance of the `NETPIE` class.

### Example

```python
from netpie import NETPIE

# Create an instance of the NETPIE class
netpie_client = NETPIE()
```

## Set NETPIE authentication details

```python
from netpie import NETPIE

# Create an instance of the NETPIE class
netpie_client = NETPIE()
netpie_client.set_profile()
```
